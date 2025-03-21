import gradio as gr
from ..tool import ProcessingTool
from ...utils import lang_labels, refresh_image_list, toggle_image_inputs
from ...processing import process_mask
from ..components import create_output_settings

class MaskTool(ProcessingTool):
    
    def __init__(self):
        super().__init__("mask")
    
    def create_tab(self, lang_dropdown):
        lang = lang_dropdown.value
        
        with gr.TabItem(label=lang_labels[lang]["mask_renderer"]) as tab:
            self.tab_titles["mask_renderer"] = (tab, "label")
            self.components["lang_dropdown"] = lang_dropdown
            
            self._create_mask_selection(lang)
            
            self._create_image_selection(lang)
            
            out_dir, out_filename = create_output_settings(lang)
            self.register_for_language_update(out_dir, "output_folder")
            self.register_for_language_update(out_filename, "output_filename")
            
            self.components["out_dir"] = out_dir
            self.components["out_filename"] = out_filename
            
            process_btn = gr.Button(lang_labels[lang]["process_mask"])
            self.register_for_language_update(process_btn, "process_mask", "value")
            self.components["process_btn"] = process_btn
            
            result_image = gr.Image(
                type="numpy",
                label=lang_labels[lang]["rendered_mask"]
            )
            self.register_for_language_update(result_image, "rendered_mask")
            self.components["result_image"] = result_image
            
            save_status = gr.Textbox(
                label=lang_labels[lang]["save_status"],
                interactive=False
            )
            self.register_for_language_update(save_status, "save_status")
            self.components["save_status"] = save_status
            
            self._bind_events()
            
        return self.components
    
    def _create_mask_selection(self, lang):
        with gr.Row():
            mask_dir = gr.Textbox(
                value="input/masks",
                label=lang_labels[lang]["mask_dir"]
            )
            self.register_for_language_update(mask_dir, "mask_dir")
            
            mask_refresh = gr.Button(lang_labels[lang]["mask_refresh"])
            self.register_for_language_update(mask_refresh, "mask_refresh", "value")
        
        mask_dropdown = gr.Dropdown(
            label=lang_labels[lang]["mask_select"],
            interactive=True,
            allow_custom_value=False
        )
        self.register_for_language_update(mask_dropdown, "mask_select")
        
        self.components["mask_dir"] = mask_dir
        self.components["mask_refresh"] = mask_refresh
        self.components["mask_dropdown"] = mask_dropdown
    
    def _create_image_selection(self, lang):
        with gr.Row():
            use_image = gr.Radio(
                choices=["No", "Yes"],
                value="No",
                label=lang_labels[lang]["use_image"]
            )
            self.register_for_language_update(use_image, "use_image")
            
            image_dir = gr.Textbox(
                value="input/",
                label=lang_labels[lang]["image_dir"],
                visible=False
            )
            self.register_for_language_update(image_dir, "image_dir")
            
            image_refresh = gr.Button(
                lang_labels[lang]["image_refresh"],
                visible=False
            )
            self.register_for_language_update(image_refresh, "image_refresh", "value")
        
        image_dropdown = gr.Dropdown(
            label=lang_labels[lang]["select_image"],
            interactive=True,
            visible=False,
            allow_custom_value=False
        )
        self.register_for_language_update(image_dropdown, "select_image")
        
        self.components["use_image"] = use_image
        self.components["image_dir"] = image_dir
        self.components["image_refresh"] = image_refresh
        self.components["image_dropdown"] = image_dropdown
    
    def _bind_events(self):
        self.components["mask_refresh"].click(
            fn=lambda d: gr.update(
                choices=refresh_image_list(d),
                value=(refresh_image_list(d)[0] if refresh_image_list(d) else None)
            ),
            inputs=[self.components["mask_dir"]],
            outputs=[self.components["mask_dropdown"]]
        )
        
        self.components["image_refresh"].click(
            fn=lambda d: gr.update(
                choices=refresh_image_list(d),
                value=(refresh_image_list(d)[0] if refresh_image_list(d) else None)
            ),
            inputs=[self.components["image_dir"]],
            outputs=[self.components["image_dropdown"]]
        )
        
        self.components["use_image"].change(
            fn=toggle_image_inputs,
            inputs=[self.components["use_image"]],
            outputs=[
                self.components["image_dir"], 
                self.components["image_refresh"], 
                self.components["image_dropdown"]
            ]
        )
        
        self.components["process_btn"].click(
            fn=process_mask,
            inputs=[
                self.components["mask_dir"],
                self.components["mask_dropdown"],
                self.components["image_dir"],
                self.components["image_dropdown"],
                self.components["use_image"],
                self.components["out_dir"],
                self.components["out_filename"],
                self.components["lang_dropdown"]
            ],
            outputs=[
                self.components["result_image"],
                self.components["save_status"]
            ]
        )