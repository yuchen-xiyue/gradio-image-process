import gradio as gr
from ..tool import ProcessingTool
from ...utils import lang_labels, on_select_image
from ...processing import process_image_crop
from ..components import create_image_selection, create_image_display, create_output_settings

class CropperTool(ProcessingTool):
    """图片裁剪工具类"""
    
    def __init__(self):
        super().__init__("cropper")
    
    def create_tab(self, lang_dropdown):
        """创建图像裁剪器标签页"""
        lang = lang_dropdown.value
        
        with gr.TabItem(label=lang_labels[lang]["image_cropper"]) as tab:
            self.tab_titles["image_cropper"] = (tab, "label")
            
            # 基本信息
            self.components["lang_dropdown"] = lang_dropdown
            
            # 图片选择
            dir_text, image_list, refresh_btn = create_image_selection(lang)
            self.register_for_language_update(dir_text, "input_folder")
            self.register_for_language_update(image_list, "select_image")
            self.register_for_language_update(refresh_btn, "refresh_list", "value")
            
            self.components["dir_text"] = dir_text
            self.components["image_list"] = image_list
            self.components["refresh_btn"] = refresh_btn
            
            # 图片显示
            input_image, output_image = create_image_display(interactive=True)
            self.register_for_language_update(input_image, "input_image")
            self.register_for_language_update(output_image, "output_image")
            
            self.components["input_image"] = input_image
            self.components["output_image"] = output_image
            
            # 裁剪控制
            self.components["crop"] = self._create_crop_controls(lang)
            
            # 处理参数
            self.components["process"] = self._create_process_controls(lang)
            
            # 批处理
            self.components["batch"] = self._create_batch_controls(lang)
            
            # 输出设置
            out_dir, out_filename = create_output_settings(lang)
            self.register_for_language_update(out_dir, "output_folder")
            self.register_for_language_update(out_filename, "output_filename")
            
            self.components["out_dir"] = out_dir
            self.components["out_filename"] = out_filename
            
            # 处理按钮
            process_btn = gr.Button(lang_labels[lang]["process_crop"])
            self.register_for_language_update(process_btn, "process_crop", "value")
            self.components["process_btn"] = process_btn
            
            # 保存状态
            save_status = gr.Textbox(
                label=lang_labels[lang]["save_status"],
                interactive=False
            )
            self.register_for_language_update(save_status, "save_status")
            self.components["save_status"] = save_status
            
            # 绑定事件
            # 图片选择
            image_list.change(
                fn=on_select_image,
                inputs=[dir_text, image_list],
                outputs=[input_image]
            )
            
            # 裁剪处理
            process_btn.click(
                fn=process_image_crop,
                inputs=[
                    dir_text,
                    image_list,
                    self.components["crop"]["top"],
                    self.components["crop"]["bottom"],
                    self.components["crop"]["left"],
                    self.components["crop"]["right"],
                    self.components["process"]["target_size"],
                    self.components["process"]["output_square"],
                    self.components["process"]["margin"],
                    self.components["batch"]["process"],
                    self.components["batch"]["folder"],
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
    
    def _create_crop_controls(self, lang):
        """创建裁剪控制滑块"""
        with gr.Row():
            with gr.Column():
                crop_top = gr.Slider(
                    label=lang_labels[lang]["crop_top"], 
                    minimum=0, maximum=1000, step=1, value=0
                )
                self.register_for_language_update(crop_top, "crop_top")
                
                crop_bottom = gr.Slider(
                    label=lang_labels[lang]["crop_bottom"],
                    minimum=0, maximum=1000, step=1, value=0
                )
                self.register_for_language_update(crop_bottom, "crop_bottom")
                
            with gr.Column():
                crop_left = gr.Slider(
                    label=lang_labels[lang]["crop_left"],
                    minimum=0, maximum=1000, step=1, value=0
                )
                self.register_for_language_update(crop_left, "crop_left")
                
                crop_right = gr.Slider(
                    label=lang_labels[lang]["crop_right"],
                    minimum=0, maximum=1000, step=1, value=0
                )
                self.register_for_language_update(crop_right, "crop_right")
                
        return {
            "top": crop_top,
            "bottom": crop_bottom,
            "left": crop_left,
            "right": crop_right
        }
    
    def _create_process_controls(self, lang):
        """创建处理参数控制"""
        with gr.Row():
            target_size = gr.Slider(
                label=lang_labels[lang]["target_crop_size"],
                minimum=64, maximum=2048, step=10, value=512
            )
            self.register_for_language_update(target_size, "target_crop_size")
            
            output_square = gr.Checkbox(
                label=lang_labels[lang]["crop_square"],
                value=True
            )
            self.register_for_language_update(output_square, "crop_square")
        
        with gr.Row():
            margin = gr.Slider(
                label=lang_labels[lang]["crop_margins"],
                minimum=0, maximum=100, step=1, value=0
            )
            self.register_for_language_update(margin, "crop_margins")
        
        return {
            "target_size": target_size,
            "output_square": output_square,
            "margin": margin
        }
    
    def _create_batch_controls(self, lang):
        """创建批处理控制"""
        with gr.Row():
            batch_process = gr.Checkbox(
                label=lang_labels[lang]["batch_process"],
                value=False
            )
            self.register_for_language_update(batch_process, "batch_process")
            
            batch_folder = gr.Textbox(
                label=lang_labels[lang]["batch_folder"],
                value="input",
                visible=False
            )
            self.register_for_language_update(batch_folder, "batch_folder")
            
            # 绑定批处理文件夹可见性
            batch_process.change(
                fn=lambda x: gr.update(visible=x),
                inputs=[batch_process],
                outputs=[batch_folder]
            )
            
        return {
            "process": batch_process,
            "folder": batch_folder
        }