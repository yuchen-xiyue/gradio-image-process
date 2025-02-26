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
        
        resizer_tool = ResizerTool()
        cropper_tool = CropperTool()
        mask_tool = MaskTool()
        tools = [resizer_tool, cropper_tool, mask_tool]
        
        with gr.Tabs() as tabs:
            resizer = resizer_tool.create_tab(lang_dropdown)
            cropper = cropper_tool.create_tab(lang_dropdown)
            mask = mask_tool.create_tab(lang_dropdown)
        
        def on_language_change(lang):
            return update_ui_language_dynamic(lang, tools, title)
        
        all_outputs = [title]  
        for tool in tools:
            for comp, _, _ in tool.language_components:  
                all_outputs.append(comp)

        lang_dropdown.change(
            fn=on_language_change,
            inputs=[lang_dropdown],
            outputs=all_outputs
        )
        
        return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.queue().launch(debug=True)