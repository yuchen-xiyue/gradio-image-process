import gradio as gr
from utils import lang_labels, refresh_list, on_select_image
from processing import process_image_aspect, process_image_custom

# ---------------------------
# Callback to Update UI Labels Dynamically
# ---------------------------
def update_ui_language(lang):
    """
    When the language selection changes, update the labels of various UI components.
    Returns updated values for the title markdown and for components that support update.
    """
    messages = lang_labels[lang]
    # 返回顺序必须与下方 outputs 顺序一致
    return (
        gr.update(value=f"# {messages['title']}"),                # title_markdown
        gr.update(label=messages["input_folder"]),                 # dir_text
        gr.update(value=messages["refresh_list"]),                 # refresh_btn (button text via value)
        gr.update(label=messages["select_image"]),                 # image_list
        gr.update(label=messages["input_image"]),                  # input_image
        gr.update(label=messages["output_image"]),                 # output_image
        gr.update(label=messages["target_size"]),                  # target_size_slider
        gr.update(label=messages["output_square"]),                # output_square_checkbox
        gr.update(value=messages["process_aspect"]),               # process_aspect_btn (button text via value)
        gr.update(label=messages["target_width"]),                 # target_width_slider
        gr.update(label=messages["target_height"]),                # target_height_slider
        gr.update(value=messages["process_custom"]),               # process_custom_btn (button text via value)
        gr.update(label=messages["apply_binary"]),                 # apply_binary_checkbox
        gr.update(label=messages["binary_threshold"]),             # binary_threshold_slider
        gr.update(label=messages["output_folder"]),                # out_dir_text
        gr.update(label=messages["output_filename"]),              # out_filename_text
        gr.update(label=messages["save_status"])                   # save_status
    )

# ---------------------------
# Build Gradio UI
# ---------------------------
with gr.Blocks() as demo:
    # Title Markdown (initially English)
    title_markdown = gr.Markdown(f"# {lang_labels['English']['title']}")
    
    # Language selector (affects UI labels and messages)
    lang_dropdown = gr.Dropdown(choices=["English", "中文"],
                                value="English",
                                label=lang_labels["English"]["language"])
    
    # ----- Image Selection Area -----
    with gr.Row():
        dir_text = gr.Textbox(label=lang_labels["English"]["input_folder"], value="input")
        image_list = gr.Dropdown(label=lang_labels["English"]["select_image"], choices=[], interactive=True)
        refresh_btn = gr.Button(lang_labels["English"]["refresh_list"])
    
    # ----- Display Input and Output Images Side by Side -----
    with gr.Row():
        input_image = gr.Image(label=lang_labels["English"]["input_image"], type="pil")
        output_image = gr.Image(label=lang_labels["English"]["output_image"], type="pil")
    
    # ----- Processing Parameters: Tabs for Different Modes -----
    with gr.Tabs():
        with gr.Tab(lang_labels["English"]["aspect_tab"]):
            with gr.Column():
                target_size_slider = gr.Slider(label=lang_labels["English"]["target_size"],
                                               minimum=64, maximum=2048, step=10, value=512)
                # Default output square is enabled
                output_square_checkbox = gr.Checkbox(label=lang_labels["English"]["output_square"], value=True)
                process_aspect_btn = gr.Button(lang_labels["English"]["process_aspect"])
        with gr.Tab(lang_labels["English"]["custom_tab"]):
            with gr.Column():
                target_width_slider = gr.Slider(label=lang_labels["English"]["target_width"],
                                                minimum=64, maximum=2048, step=10, value=512)
                target_height_slider = gr.Slider(label=lang_labels["English"]["target_height"],
                                                 minimum=64, maximum=2048, step=10, value=512)
                process_custom_btn = gr.Button(lang_labels["English"]["process_custom"])
    
    # ----- Common Options: Binary Conversion Settings -----
    with gr.Row():
        apply_binary_checkbox = gr.Checkbox(label=lang_labels["English"]["apply_binary"], value=False)
        # Binary threshold slider: UI value from 0 to 1 (will be converted internally)
        binary_threshold_slider = gr.Slider(label=lang_labels["English"]["binary_threshold"],
                                            minimum=0, maximum=1, step=0.01, value=0.5)
    
    # ----- Output Saving Settings -----
    with gr.Row():
        out_dir_text = gr.Textbox(label=lang_labels["English"]["output_folder"], value="output")
        out_filename_text = gr.Textbox(label=lang_labels["English"]["output_filename"], value="")
    
    # ----- Save Status (Read-only) -----
    save_status = gr.Textbox(label=lang_labels["English"]["save_status"], value="", interactive=False)
    
    # ---------------------------
    # Bindings
    # ---------------------------
    # When language selection changes, update UI labels.
    lang_dropdown.change(
        fn=update_ui_language,
        inputs=lang_dropdown,
        outputs=[title_markdown, dir_text, refresh_btn, image_list,
                 input_image, output_image, target_size_slider, output_square_checkbox,
                 process_aspect_btn, target_width_slider, target_height_slider,
                 process_custom_btn, apply_binary_checkbox, binary_threshold_slider,
                 out_dir_text, out_filename_text, save_status]
    )
    
    # Refresh image list based on input folder.
    refresh_btn.click(fn=refresh_list, inputs=dir_text, outputs=image_list)
    
    # When an image is selected, load and display it.
    image_list.change(fn=on_select_image, inputs=[dir_text, image_list], outputs=input_image)
    
    # Process image in Aspect Rescale mode.
    process_aspect_btn.click(
        fn=process_image_aspect,
        inputs=[dir_text, image_list, target_size_slider, output_square_checkbox,
                out_dir_text, out_filename_text, apply_binary_checkbox,
                binary_threshold_slider, lang_dropdown],
        outputs=[output_image, save_status]
    )
    
    # Process image in Custom Resize mode.
    process_custom_btn.click(
        fn=process_image_custom,
        inputs=[dir_text, image_list, target_width_slider, target_height_slider,
                out_dir_text, out_filename_text, apply_binary_checkbox,
                binary_threshold_slider, lang_dropdown],
        outputs=[output_image, save_status]
    )

if __name__ == '__main__':
    demo.launch()
