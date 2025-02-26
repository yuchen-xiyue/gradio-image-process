import gradio as gr
from src.ui.tabs.resizer import ResizerTool
from src.ui.tabs.cropper import CropperTool
from src.ui.tabs.mask import MaskTool
from src.utils import lang_labels, update_ui_language_dynamic

def create_ui():
    """Create the main UI"""
    with gr.Blocks(title="Image Processing Tool") as demo:
        title = gr.Markdown(f"# {lang_labels['English']['title']}")
        
        lang_dropdown = gr.Dropdown(
            choices=["English", "中文"],
            value="English",
            label=lang_labels["English"]["language"],
            container=False
        )
        
        # 创建工具实例
        resizer_tool = ResizerTool()
        cropper_tool = CropperTool()
        mask_tool = MaskTool()
        tools = [resizer_tool, cropper_tool, mask_tool]
        
        # 创建选项卡
        with gr.Tabs() as tabs:
            resizer = resizer_tool.create_tab(lang_dropdown)
            cropper = cropper_tool.create_tab(lang_dropdown)
            mask = mask_tool.create_tab(lang_dropdown)
        
        # 使用新的动态语言更新系统
        def on_language_change(lang):
            # 直接返回更新列表，不要使用字典
            return update_ui_language_dynamic(lang, tools, title)
        
        # 收集所有可用于事件输出的组件（不包括Tab）
        all_outputs = [title]  # 先添加标题
        for tool in tools:
            # 只添加非Tab组件
            for comp, _, _ in tool.language_components:  # 这里已经不包含Tab组件了
                all_outputs.append(comp)

        # 更新TabItem的标题需要在Gradio 5.x中使用不同方式，需要后续开发
        lang_dropdown.change(
            fn=on_language_change,
            inputs=[lang_dropdown],
            outputs=all_outputs
        )
        
        return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.queue().launch(debug=True)