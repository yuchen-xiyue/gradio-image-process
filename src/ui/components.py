import gradio as gr
from ..utils import lang_labels, refresh_list

def create_image_selection(lang="English"):
    """Create directory input, image selection dropdown and refresh button"""
    with gr.Row():
        dir_text = gr.Textbox(
            label=lang_labels[lang]["input_folder"], 
            value="input"
        )
        image_list = gr.Dropdown(
            label=lang_labels[lang]["select_image"], 
            interactive=True,
            allow_custom_value=False
        )
        refresh_btn = gr.Button(lang_labels[lang]["refresh_list"])
        
    refresh_btn.click(
        fn=refresh_list,
        inputs=[dir_text],
        outputs=[image_list]
    )
    
    return dir_text, image_list, refresh_btn

def create_image_display(interactive=False):
    """Create input and output image display components"""
    with gr.Row():
        input_image = gr.Image(
            label="Input Image",
            type="pil",
            interactive=interactive
        )
        output_image = gr.Image(
            label="Output Image",
            format="png",
            type="pil"
        )
    return input_image, output_image

def create_output_settings(lang="English"):
    """Create output directory and filename inputs"""
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