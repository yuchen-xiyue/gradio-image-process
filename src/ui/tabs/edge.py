import gradio as gr

from ..components import create_image_selection, create_image_display, create_output_settings
from ..tool import ProcessingTool
from ...utils import lang_labels
from ...processing.edge import process_edge_detection

class EdgeDetectionTool(ProcessingTool):
    
    def __init__(self):
        super().__init__("edge")
        self.tab_titles = {}
    
    def create_tab(self, lang_dropdown):
        lang = lang_dropdown.value
        
        with gr.TabItem(label=lang_labels[lang]["edge_detection_tool"]) as tab:
            self.tab_titles["edge_detection_tool"] = (tab, "label")
            
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
            
            self.components["edge_params"] = self._create_edge_controls(lang)
            
            out_dir, out_filename = create_output_settings(lang)
            self.register_for_language_update(out_dir, "output_folder")
            self.register_for_language_update(out_filename, "output_filename")
            
            self.components["out_dir"] = out_dir
            self.components["out_filename"] = out_filename
            
            process_btn = gr.Button(lang_labels[lang]["process_edge"])
            self.register_for_language_update(process_btn, "process_edge", "value")
            self.components["process_btn"] = process_btn
            
            save_status = gr.Textbox(
                label=lang_labels[lang]["save_status"],
                interactive=False
            )
            self.register_for_language_update(save_status, "save_status")
            self.components["save_status"] = save_status
            
            image_list.change(
                fn=self._on_select_image,
                inputs=[dir_text, image_list],
                outputs=[input_image]
            )
            
            process_btn.click(
                fn=process_edge_detection,
                inputs=[
                    dir_text,
                    image_list,
                    self.components["edge_params"]["algorithm"],
                    self.components["edge_params"]["canny_low"],
                    self.components["edge_params"]["canny_high"],
                    self.components["edge_params"]["sigma"],
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
    
    def _create_edge_controls(self, lang):
        with gr.Accordion(label=lang_labels[lang]["edge_parameters"], open=True):
            with gr.Row():
                algorithm = gr.Radio(
                    choices=["Roberts", "Sobel", "Prewitt", "Laplacian", "LoG", "Canny"],
                    value="Sobel",
                    label=lang_labels[lang]["edge_algorithm"]
                )
                self.register_for_language_update(algorithm, "edge_algorithm")
                
            with gr.Row():
                with gr.Column():
                    canny_low = gr.Slider(
                        label=lang_labels[lang]["canny_low_threshold"],
                        minimum=0, maximum=255, step=1, value=50,
                        visible=False
                    )
                    self.register_for_language_update(canny_low, "canny_low_threshold")
                    
                with gr.Column():
                    canny_high = gr.Slider(
                        label=lang_labels[lang]["canny_high_threshold"],
                        minimum=0, maximum=255, step=1, value=150,
                        visible=False
                    )
                    self.register_for_language_update(canny_high, "canny_high_threshold")
            
            with gr.Row():
                sigma = gr.Slider(
                    label=lang_labels[lang]["gaussian_sigma"],
                    minimum=0.1, maximum=5.0, step=0.1, value=1.0,
                    visible=False
                )
                self.register_for_language_update(sigma, "gaussian_sigma")
            
            algorithm.change(
                fn=self._update_parameter_visibility,
                inputs=[algorithm],
                outputs=[canny_low, canny_high, sigma]
            )
                
        return {
            "algorithm": algorithm,
            "canny_low": canny_low,
            "canny_high": canny_high,
            "sigma": sigma
        }
    
    def _update_parameter_visibility(self, algorithm):
        show_canny = algorithm == "Canny"
        show_sigma = algorithm in ["LoG"]
        
        return (
            gr.update(visible=show_canny),
            gr.update(visible=show_canny),
            gr.update(visible=show_sigma)
        )
    
    def _on_select_image(self, directory, filename):
        from ...utils.files import on_select_image
        return on_select_image(directory, filename)