from abc import ABC, abstractmethod
from ..utils import lang_labels

class ProcessingTool(ABC):
    """抽象基类，所有处理工具继承此类"""
    
    def __init__(self, tool_type):
        self.components = {}
        self.tool_type = tool_type
        self.language_components = []  # 存储需要语言更新的组件及其信息
        self.tab_titles = {}  # 存储选项卡标题，但不注册为组件
    
    @abstractmethod
    def create_tab(self, lang_dropdown):
        """创建工具标签页并返回组件"""
        pass
    
    def register_for_language_update(self, component, lang_key, update_type="label"):
        """注册组件进行语言更新
        
        Args:
            component: 要更新的UI组件
            lang_key: 语言标签字典中的键名
            update_type: 更新类型（"label"或"value"）
        """
        if component is not None:
            # 检查是否为Tab对象或TabItem对象
            component_type = type(component).__name__
            if component_type in ["Tab", "TabItem"]:
                # 不注册Tab/TabItem，但记录其标题用于调试
                self.tab_titles[lang_key] = (component, update_type)
            else:
                # 正常注册其他组件
                self.language_components.append((component, lang_key, update_type))
        return component
    
    def get_language_updates(self, lang):
        """获取语言更新值列表"""
        import gradio as gr
        updates = []
        
        # 只为非Tab组件生成更新
        for component, lang_key, update_type in self.language_components:
            if lang_key in lang_labels[lang]:
                if update_type == "label":
                    updates.append(gr.update(label=lang_labels[lang][lang_key]))
                else:
                    updates.append(gr.update(value=lang_labels[lang][lang_key]))
        
        return updates