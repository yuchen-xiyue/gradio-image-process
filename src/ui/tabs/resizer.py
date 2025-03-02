import gradio as gr
from ..tool import ProcessingTool
from ...utils import lang_labels, on_select_image
from ...processing import process_image_aspect, process_image_custom
from ..components import create_image_selection, create_image_display, create_output_settings

class ResizerTool(ProcessingTool):
    
    def __init__(self):
        super().__init__("resizer")
    
    def create_tab(self, lang_dropdown):
        lang = lang_dropdown.value
        
        with gr.TabItem(label=lang_labels[lang]["image_resizer"]) as tab:
            self.tab_titles["image_resizer"] = (tab, "label")
                
            self.components["lang_dropdown"] = lang_dropdown
            
            dir_text, image_list, refresh_btn = create_image_selection(lang)
            self.register_for_language_update(dir_text, "input_folder")
            self.register_for_language_update(image_list, "select_image")
            self.register_for_language_update(refresh_btn, "refresh_list", "value")
            
            self.components["dir_text"] = dir_text
            self.components["image_list"] = image_list
            self.components["refresh_btn"] = refresh_btn
            
            input_image, output_image = create_image_display()
            self.register_for_language_update(input_image, "input_image")
            self.register_for_language_update(output_image, "output_image")
            
            self.components["input_image"] = input_image
            self.components["output_image"] = output_image
            
            out_dir, out_filename = create_output_settings(lang)
            self.register_for_language_update(out_dir, "output_folder")
            self.register_for_language_update(out_filename, "output_filename")
            
            self.components["out_dir"] = out_dir
            self.components["out_filename"] = out_filename
            
            save_status = gr.Textbox(
                label=lang_labels[lang]["save_status"],
                interactive=False
            )
            self.register_for_language_update(save_status, "save_status")
            self.components["save_status"] = save_status
            
            with gr.Accordion("Advanced Options", open=False):
                self.components["binary"] = self._create_binary_controls(lang)
                self.components["blur"] = self._create_blur_controls(lang)
            
            with gr.Tabs():
                with gr.TabItem(label=lang_labels[lang]["aspect_tab"]) as aspect_tab:
                    self.tab_titles["aspect_tab"] = (aspect_tab, "label")
                    self.components["aspect"] = self._create_aspect_tab(lang)
                    
                with gr.TabItem(label=lang_labels[lang]["custom_tab"]) as custom_tab:
                    self.tab_titles["custom_tab"] = (custom_tab, "label")
                    self.components["custom"] = self._create_custom_tab(lang)
            
            image_list.change(
                fn=on_select_image,
                inputs=[dir_text, image_list],
                outputs=[input_image]
            )
            
        return self.components
    
    def _create_aspect_tab(self, lang):
        with gr.Column():
            target_size = gr.Slider(
                label=lang_labels[lang]["target_size"],
                minimum=64, maximum=2048, step=10, value=512
            )
            self.register_for_language_update(target_size, "target_size")
            
            output_square = gr.Checkbox(
                label=lang_labels[lang]["output_square"],
                value=True
            )
            self.register_for_language_update(output_square, "output_square")
            
            margin = gr.Slider(
                label=lang_labels[lang]["margin"],
                minimum=0, maximum=256, step=0.1, value=0
            )
            self.register_for_language_update(margin, "margin")
            
            process_btn = gr.Button(lang_labels[lang]["process_aspect"])
            self.register_for_language_update(process_btn, "process_aspect", "value")
            
            process_btn.click(
                fn=process_image_aspect,
                inputs=[
                    self.components["dir_text"],
                    self.components["image_list"],
                    target_size,
                    output_square,
                    self.components["out_dir"],
                    self.components["out_filename"],
                    self.components["binary"]["apply"],
                    self.components["binary"]["threshold"],
                    margin,
                    self.components["blur"]["apply"],
                    self.components["blur"]["radius"],
                    self.components["lang_dropdown"]
                ],
                outputs=[
                    self.components["output_image"],
                    self.components["save_status"]
                ]
            )
        
        return {
            "target_size": target_size,
            "output_square": output_square,
            "margin": margin,
            "process_btn": process_btn
        }
    
    def _create_custom_tab(self, lang):
        with gr.Column():
            width = gr.Slider(
                label=lang_labels[lang]["target_width"],
                minimum=64, maximum=2048, step=10, value=512
            )
            self.register_for_language_update(width, "target_width")
            
            height = gr.Slider(
                label=lang_labels[lang]["target_height"],
                minimum=64, maximum=2048, step=10, value=512
            )
            self.register_for_language_update(height, "target_height")
            
            process_btn = gr.Button(lang_labels[lang]["process_custom"])
            self.register_for_language_update(process_btn, "process_custom", "value")
            
            process_btn.click(
                fn=process_image_custom,
                inputs=[
                    self.components["dir_text"],
                    self.components["image_list"],
                    width,
                    height,
                    self.components["out_dir"],
                    self.components["out_filename"],
                    self.components["binary"]["apply"],
                    self.components["binary"]["threshold"],
                    self.components["blur"]["apply"],
                    self.components["blur"]["radius"],
                    self.components["lang_dropdown"]
                ],
                outputs=[
                    self.components["output_image"],
                    self.components["save_status"]
                ]
            )
        
        return {
            "width": width,
            "height": height,
            "process_btn": process_btn
        }
    
    def _create_binary_controls(self, lang):
        with gr.Row():
            apply = gr.Checkbox(
                label=lang_labels[lang]["apply_binary"],
                value=False
            )
            self.register_for_language_update(apply, "apply_binary")
            
            threshold = gr.Slider(
                label=lang_labels[lang]["binary_threshold"],
                minimum=0, maximum=1, step=0.01, value=0.5
            )
            self.register_for_language_update(threshold, "binary_threshold")
            
        return {
            "apply": apply,
            "threshold": threshold
        }
    
    def _create_blur_controls(self, lang):
        with gr.Row():
            apply = gr.Checkbox(
                label=lang_labels[lang]["apply_blur"],
                value=False
            )
            self.register_for_language_update(apply, "apply_blur")
            
            radius = gr.Slider(
                label=lang_labels[lang]["blur_radius"],
                minimum=0.1, maximum=10, step=0.1, value=1
            )
            self.register_for_language_update(radius, "blur_radius")
            
        return {
            "apply": apply,
            "radius": radius
        }