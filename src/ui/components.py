import gradio as gr
from ..utils import lang_labels

def create_image_selection(lang="English", prefix=""):
    """Create standard image selection row"""
    with gr.Row():
        dir_text = gr.Textbox(
            label=lang_labels[lang]["input_folder"], 
            value="input"
        )
        image_list = gr.Dropdown(
            label=lang_labels[lang]["select_image"], 
            choices=[], 
            interactive=True
        )
        refresh_btn = gr.Button(lang_labels[lang]["refresh_list"])
    return dir_text, image_list, refresh_btn

def create_image_display(interactive=False):
    """Create input/output image display row"""
    with gr.Row():
        input_image = gr.Image(type="pil", interactive=interactive)
        output_image = gr.Image(type="pil")
    return input_image, output_image

def create_output_settings(lang="English"):
    """Create output settings row"""
    with gr.Row():
        out_dir = gr.Textbox(
            label=lang_labels[lang]["output_folder"], 
            value="output"
        )
        out_filename = gr.Textbox(
            label=lang_labels[lang]["output_filename"], 
            value=""
        )
    return out_dir, out_filename