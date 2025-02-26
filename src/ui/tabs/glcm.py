import gradio as gr
from ..tool import ProcessingTool
from ...utils import lang_labels, on_select_image
from ...processing import process_glcm_features
from ..components import create_image_selection, create_image_display, create_output_settings
import os
import matplotlib.pyplot as plt
import io
from PIL import Image
import numpy as np

class GLCMTool(ProcessingTool):
    
    def __init__(self):
        super().__init__("glcm")
        self.tab_titles = {}
        self.feature_maps = {}  
        self.current_image_name = None  
    
    def create_tab(self, lang_dropdown):
        lang = lang_dropdown.value
        
        with gr.TabItem(label=lang_labels[lang]["glcm_tool"]) as tab:
            self.tab_titles["glcm_tool"] = (tab, "label")
            
            self.components["lang_dropdown"] = lang_dropdown
            
            dir_text, image_list, refresh_btn = create_image_selection(lang)
            self.register_for_language_update(dir_text, "input_folder")
            self.register_for_language_update(image_list, "select_image")
            self.register_for_language_update(refresh_btn, "refresh_list", "value")
            
            self.components["dir_text"] = dir_text
            self.components["image_list"] = image_list
            self.components["refresh_btn"] = refresh_btn
            
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(type="pil", label=lang_labels[lang]["input_image"])
                    self.register_for_language_update(input_image, "input_image")
                    self.components["input_image"] = input_image
                
                with gr.Column():
                    feature_image = gr.Image(type="numpy", label=lang_labels[lang]["feature_visualization"])
                    self.register_for_language_update(feature_image, "feature_visualization")
                    self.components["feature_image"] = feature_image
            
            self.components["glcm_params"] = self._create_glcm_params(lang)
            
            self.components["feature_selection"] = self._create_feature_selection(lang)
            
            out_dir, out_filename = create_output_settings(lang)
            self.register_for_language_update(out_dir, "output_folder")
            self.register_for_language_update(out_filename, "output_filename")
            
            self.components["out_dir"] = out_dir
            self.components["out_filename"] = out_filename
            
            with gr.Row():
                with gr.Column():
                    feature_values = gr.DataFrame(
                        headers=["Feature", "Value"],
                        label=lang_labels[lang]["feature_values"],
                        interactive=False
                    )
                    self.register_for_language_update(feature_values, "feature_values")
                    self.components["feature_values"] = feature_values
            
            with gr.Row():
                process_btn = gr.Button(lang_labels[lang]["process_glcm"])
                self.register_for_language_update(process_btn, "process_glcm", "value")
                self.components["process_btn"] = process_btn
                
                save_btn = gr.Button(lang_labels[lang]["save_features"])
                self.register_for_language_update(save_btn, "save_features", "value")
                self.components["save_btn"] = save_btn
            
            status = gr.Textbox(
                label=lang_labels[lang]["save_status"],
                interactive=False
            )
            self.register_for_language_update(status, "save_status")
            self.components["status"] = status
            
            image_list.change(
                fn=on_select_image,
                inputs=[dir_text, image_list],
                outputs=[input_image]
            )
            
            process_btn.click(
                fn=self._process_glcm_wrapper,  
                inputs=[
                    dir_text,
                    image_list,
                    self.components["glcm_params"]["distance"],
                    self.components["glcm_params"]["angles"],
                    self.components["glcm_params"]["levels"],
                    self.components["glcm_params"]["symmetric"],
                    self.components["glcm_params"]["normalize"],
                    self.components["feature_selection"]["contrast"],
                    self.components["feature_selection"]["dissimilarity"],
                    self.components["feature_selection"]["homogeneity"],
                    self.components["feature_selection"]["energy"],
                    self.components["feature_selection"]["correlation"],
                    self.components["feature_selection"]["ASM"],
                    lang_dropdown
                ],
                outputs=[
                    feature_image,
                    feature_values
                ]
            )
            
            save_btn.click(
                fn=self._save_features,
                inputs=[
                    out_dir,
                    out_filename,
                    lang_dropdown
                ],
                outputs=[status]
            )
            
        return self.components
    
    def _process_glcm_wrapper(self, input_dir, filename, *args):
        # 存储当前图像名称
        self.current_image_name = filename
        
        # 调用实际处理函数
        feature_img, feature_table, feature_maps = process_glcm_features(input_dir, filename, *args)
        
        # 存储特征图
        self.feature_maps = feature_maps
        
        return feature_img, feature_table
    
    def _save_features(self, out_dir, out_filename, lang):
        from ...utils import lang_labels
        
        messages = lang_labels[lang]
        
        if not self.feature_maps or not self.current_image_name:
            return messages["no_features_to_save"]
        
        try:
            if not out_dir or out_dir.strip() == "":
                out_dir = "output/features"
            
            os.makedirs(out_dir, exist_ok=True)
            
            if not out_filename or out_filename.strip() == "":
                base = os.path.splitext(self.current_image_name)[0] if self.current_image_name else "glcm_features"
            else:
                base = os.path.splitext(out_filename)[0]
            
            saved_files = []
            
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            axes = axes.flatten()
            
            min_val = float('inf')
            max_val = float('-inf')
            for feature_map in self.feature_maps.values():
                min_val = min(min_val, np.min(feature_map))
                max_val = max(max_val, np.max(feature_map))
            
            for i, (feature_name, feature_map) in enumerate(self.feature_maps.items()):
                if i < len(axes):
                    im = axes[i].imshow(feature_map, cmap='viridis', vmin=min_val, vmax=max_val)
                    axes[i].set_title(feature_name)
                    axes[i].axis('off')
                    fig.colorbar(im, ax=axes[i], fraction=0.046, pad=0.04)
                
                feature_filename = f"{base}_{feature_name}.png"
                feature_path = os.path.join(out_dir, feature_filename)
                
                plt.figure(figsize=(8, 6))
                plt.imshow(feature_map, cmap='viridis')
                plt.colorbar(label=feature_name)
                plt.title(feature_name)
                plt.axis('off')
                plt.tight_layout()
                plt.savefig(feature_path, dpi=150, bbox_inches='tight')
                plt.close()
                
                saved_files.append(feature_filename)
            
            plt.tight_layout()
            combined_path = os.path.join(out_dir, f"{base}_combined.png")
            fig.savefig(combined_path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            saved_files.append(f"{base}_combined.png")
            
            stats_data = []
            for feature_name, feature_map in self.feature_maps.items():
                mean_val = np.mean(feature_map)
                std_val = np.std(feature_map)
                min_val = np.min(feature_map)
                max_val = np.max(feature_map)
                
                stats_data.append([
                    feature_name, 
                    f"{mean_val:.5f}",
                    f"{std_val:.5f}", 
                    f"{min_val:.5f}", 
                    f"{max_val:.5f}"
                ])
            
            import pandas as pd
            stats_df = pd.DataFrame(
                stats_data, 
                columns=["Feature", "Mean", "Std Dev", "Min", "Max"]
            )
            csv_path = os.path.join(out_dir, f"{base}_stats.csv")
            stats_df.to_csv(csv_path, index=False)
            saved_files.append(f"{base}_stats.csv")
            
            saved_list = ", ".join(saved_files)
            return messages["save_success"].format(f"{out_dir}/{saved_list}")
        
        except Exception as e:
            return messages["save_failed"].format(str(e))
    
    def _create_glcm_params(self, lang):
        with gr.Accordion(label=lang_labels[lang]["glcm_parameters"], open=True):
            with gr.Row():
                with gr.Column():
                    distance = gr.Slider(
                        label=lang_labels[lang]["glcm_distance"],
                        minimum=1, maximum=5, step=1, value=1
                    )
                    self.register_for_language_update(distance, "glcm_distance")
                
                with gr.Column():
                    angles = gr.CheckboxGroup(
                        choices=["0°", "45°", "90°", "135°"],
                        value=["0°"],
                        label=lang_labels[lang]["glcm_angles"]
                    )
                    self.register_for_language_update(angles, "glcm_angles")
            
            with gr.Row():
                with gr.Column():
                    levels = gr.Slider(
                        label=lang_labels[lang]["glcm_levels"],
                        minimum=8, maximum=256, step=8, value=64
                    )
                    self.register_for_language_update(levels, "glcm_levels")
                
                with gr.Column():
                    symmetric = gr.Checkbox(
                        label=lang_labels[lang]["glcm_symmetric"],
                        value=True
                    )
                    self.register_for_language_update(symmetric, "glcm_symmetric")
                    
                    normalize = gr.Checkbox(
                        label=lang_labels[lang]["glcm_normalize"],
                        value=True
                    )
                    self.register_for_language_update(normalize, "glcm_normalize")
        
        return {
            "distance": distance,
            "angles": angles,
            "levels": levels,
            "symmetric": symmetric,
            "normalize": normalize
        }
    
    def _create_feature_selection(self, lang):
        with gr.Accordion(label=lang_labels[lang]["feature_selection"], open=True):
            with gr.Row():
                with gr.Column():
                    contrast = gr.Checkbox(
                        label=lang_labels[lang]["feature_contrast"],
                        value=True
                    )
                    self.register_for_language_update(contrast, "feature_contrast")
                    
                    dissimilarity = gr.Checkbox(
                        label=lang_labels[lang]["feature_dissimilarity"],
                        value=True
                    )
                    self.register_for_language_update(dissimilarity, "feature_dissimilarity")
                
                with gr.Column():
                    homogeneity = gr.Checkbox(
                        label=lang_labels[lang]["feature_homogeneity"],
                        value=True
                    )
                    self.register_for_language_update(homogeneity, "feature_homogeneity")
                    
                    energy = gr.Checkbox(
                        label=lang_labels[lang]["feature_energy"],
                        value=True
                    )
                    self.register_for_language_update(energy, "feature_energy")
                
                with gr.Column():
                    correlation = gr.Checkbox(
                        label=lang_labels[lang]["feature_correlation"],
                        value=True
                    )
                    self.register_for_language_update(correlation, "feature_correlation")
                    
                    ASM = gr.Checkbox(
                        label=lang_labels[lang]["feature_asm"],
                        value=True
                    )
                    self.register_for_language_update(ASM, "feature_asm")
        
        return {
            "contrast": contrast,
            "dissimilarity": dissimilarity,
            "homogeneity": homogeneity,
            "energy": energy,
            "correlation": correlation,
            "ASM": ASM
        }
