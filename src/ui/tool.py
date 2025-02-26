from abc import ABC, abstractmethod
from ..utils import lang_labels

class ProcessingTool(ABC):
    
    def __init__(self, tool_type):
        self.components = {}
        self.tool_type = tool_type
        self.language_components = []  
        self.tab_titles = {} 
    
    @abstractmethod
    def create_tab(self, lang_dropdown):
        pass
    
    def register_for_language_update(self, component, lang_key, update_type="label"):
        if component is not None:
            component_type = type(component).__name__
            if component_type in ["Tab", "TabItem"]:
                self.tab_titles[lang_key] = (component, update_type)
            else:
                self.language_components.append((component, lang_key, update_type))
        return component
    
    def get_language_updates(self, lang):
        import gradio as gr
        updates = []
        
        for component, lang_key, update_type in self.language_components:
            if lang_key in lang_labels[lang]:
                if update_type == "label":
                    updates.append(gr.update(label=lang_labels[lang][lang_key]))
                else:
                    updates.append(gr.update(value=lang_labels[lang][lang_key]))
        
        return updates