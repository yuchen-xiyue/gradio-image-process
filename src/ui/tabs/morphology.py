import gradio as gr
from ..tool import ProcessingTool
from ...utils import lang_labels, on_select_image
from ...processing import process_morphology
from ..components import create_image_selection, create_image_display, create_output_settings

class MorphologyTool(ProcessingTool):
    
    def __init__(self):
        super().__init__("morphology")
        self.tab_titles = {}
    
    def create_tab(self, lang_dropdown):
        lang = lang_dropdown.value
        
        with gr.TabItem(label=lang_labels[lang]["morphology_tool"]) as tab:
            self.tab_titles["morphology_tool"] = (tab, "label")
            
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
            
            self.components["morphology"] = self._create_morphology_controls(lang)
            
            out_dir, out_filename = create_output_settings(lang)
            self.register_for_language_update(out_dir, "output_folder")
            self.register_for_language_update(out_filename, "output_filename")
            
            self.components["out_dir"] = out_dir
            self.components["out_filename"] = out_filename
            
            process_btn = gr.Button(lang_labels[lang]["process_morph"])
            self.register_for_language_update(process_btn, "process_morph", "value")
            self.components["process_btn"] = process_btn
            
            save_status = gr.Textbox(
                label=lang_labels[lang]["save_status"],
                interactive=False
            )
            self.register_for_language_update(save_status, "save_status")
            self.components["save_status"] = save_status
            
            image_list.change(
                fn=on_select_image,
                inputs=[dir_text, image_list],
                outputs=[input_image]
            )
            
            process_btn.click(
                fn=process_morphology,
                inputs=[
                    dir_text,
                    image_list,
                    self.components["morphology"]["erosion"]["apply"],
                    self.components["morphology"]["erosion"]["kernel_size"],
                    self.components["morphology"]["dilation"]["apply"],
                    self.components["morphology"]["dilation"]["kernel_size"],
                    self.components["morphology"]["opening"]["apply"],
                    self.components["morphology"]["opening"]["kernel_size"],
                    self.components["morphology"]["closing"]["apply"],
                    self.components["morphology"]["closing"]["kernel_size"],
                    out_dir,
                    out_filename,
                    lang_dropdown
                ],
                outputs=[
                    output_image,
                    save_status
                ]
            )
            
        return self.components
    
    def _create_morphology_controls(self, lang):
        morphology_controls = {}
        
        with gr.Accordion("Morphological Operations", open=True):
            # 侵蚀 (Erosion)
            with gr.Row():
                with gr.Row(scale=1):
                    with gr.Column():
                        erosion_apply = gr.Radio(
                            choices=["Yes", "No"],
                            value="No",
                            label=lang_labels[lang]["apply_erosion"]
                        )
                        self.register_for_language_update(erosion_apply, "apply_erosion")
                
                
                with gr.Row(scale=1):
                    with gr.Column():
                        erosion_kernel = gr.Slider(
                            label=lang_labels[lang]["kernel_size"],
                            minimum=1, maximum=15, step=2, value=3
                        )
                        self.register_for_language_update(erosion_kernel, "kernel_size")
            
            # 膨胀 (Dilation)
                with gr.Row(scale=1):
                    with gr.Column():
                        dilation_apply = gr.Radio(
                            choices=["Yes", "No"],
                            value="No",
                            label=lang_labels[lang]["apply_dilation"]
                        )
                        self.register_for_language_update(dilation_apply, "apply_dilation")
                
                with gr.Row(scale=1):
                    with gr.Column():
                        dilation_kernel = gr.Slider(
                            label=lang_labels[lang]["kernel_size"],
                            minimum=1, maximum=15, step=2, value=3
                        )
                        self.register_for_language_update(dilation_kernel, "kernel_size")
            
            # 开运算 (Opening)
            with gr.Row():
                with gr.Row(scale=1):
                    with gr.Column():
                        opening_apply = gr.Radio(
                            choices=["Yes", "No"],
                            value="No",
                            label=lang_labels[lang]["apply_opening"]
                        )
                        self.register_for_language_update(opening_apply, "apply_opening")
                
                with gr.Row(scale=1):
                    with gr.Column():
                        opening_kernel = gr.Slider(
                            label=lang_labels[lang]["kernel_size"],
                            minimum=1, maximum=15, step=2, value=3
                        )
                        self.register_for_language_update(opening_kernel, "kernel_size")
            
            # 闭运算 (Closing)
                with gr.Row(scale=1):
                    with gr.Column():
                        closing_apply = gr.Radio(
                            choices=["Yes", "No"],
                            value="No",
                            label=lang_labels[lang]["apply_closing"]
                        )
                        self.register_for_language_update(closing_apply, "apply_closing")
                
                with gr.Row(scale=1):
                    with gr.Column():
                        closing_kernel = gr.Slider(
                            label=lang_labels[lang]["kernel_size"],
                            minimum=1, maximum=15, step=2, value=3
                        )
                        self.register_for_language_update(closing_kernel, "kernel_size")
            
        morphology_controls["erosion"] = {
            "apply": erosion_apply,
            "kernel_size": erosion_kernel
        }
        
        morphology_controls["dilation"] = {
            "apply": dilation_apply,
            "kernel_size": dilation_kernel
        }
        
        morphology_controls["opening"] = {
            "apply": opening_apply,
            "kernel_size": opening_kernel
        }
        
        morphology_controls["closing"] = {
            "apply": closing_apply,
            "kernel_size": closing_kernel
        }
        
        return morphology_controls