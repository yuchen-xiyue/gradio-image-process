import gradio as gr
from ..utils import refresh_list, on_select_image, refresh_image_list, toggle_image_inputs
from ..processing import process_image_aspect, process_image_custom, process_image_crop, process_mask

def bind_resizer_events(components, lang_dropdown):
    """Bind events for resizer tab"""
    events = []
    
    # Refresh image list
    events.append(
        components["refresh_btn"].click(
            fn=refresh_list,
            inputs=[components["dir_text"]],
            outputs=[components["image_list"]],
            api_name="refresh_resizer"
        )
    )
    
    # Load selected image
    events.append(
        components["image_list"].change(
            fn=on_select_image,
            inputs=[components["dir_text"], components["image_list"]],
            outputs=[components["input_image"]],
            api_name="select_resizer_image"
        )
    )
    
    # Process aspect mode
    events.append(
        components["aspect"]["process_btn"].click(
            fn=process_image_aspect,
            inputs=[
                components["dir_text"],
                components["image_list"],
                components["aspect"]["target_size"],
                components["aspect"]["output_square"],
                components["out_dir"],
                components["out_filename"],
                components["binary"]["apply"],
                components["binary"]["threshold"],
                components["aspect"]["margin"],
                components["blur"]["apply"],
                components["blur"]["radius"],
                lang_dropdown
            ],
            outputs=[
                components["output_image"],
                components["save_status"]
            ],
            api_name="process_aspect"
        )
    )
    
    # Process custom mode
    events.append(
        components["custom"]["process_btn"].click(
            fn=process_image_custom,
            inputs=[
                components["dir_text"],
                components["image_list"],
                components["custom"]["width"],
                components["custom"]["height"],
                components["out_dir"],
                components["out_filename"],
                components["binary"]["apply"],
                components["binary"]["threshold"],
                components["blur"]["apply"],
                components["blur"]["radius"],
                lang_dropdown
            ],
            outputs=[
                components["output_image"],
                components["save_status"]
            ],
            api_name="process_custom"
        )
    )
    
    return events

def bind_cropper_events(components, lang_dropdown):
    events = []
    
    events.append(
        components["refresh_btn"].click(
            fn=refresh_list,
            inputs=[components["dir_text"]],
            outputs=[components["image_list"]],
            api_name="refresh_cropper"
        )
    )
    
    events.append(
        components["image_list"].change(
            fn=on_select_image,
            inputs=[components["dir_text"], components["image_list"]],
            outputs=[components["input_image"]],
            api_name="select_cropper_image"
        )
    )
    
    events.append(
        components["batch"]["process"].change(
            fn=lambda x: gr.update(visible=x),
            inputs=[components["batch"]["process"]],
            outputs=[components["batch"]["folder"]],
            api_name="toggle_batch_folder"
        )
    )
    
    events.append(
        components["process_btn"].click(
            fn=process_image_crop,
            inputs=[
                components["dir_text"],
                components["image_list"],
                components["crop"]["top"],
                components["crop"]["bottom"],
                components["crop"]["left"],
                components["crop"]["right"],
                components["process"]["target_size"],
                components["process"]["output_square"],
                components["process"]["margin"],
                components["batch"]["process"],
                components["batch"]["folder"],
                components["out_dir"],
                components["out_filename"], 
                lang_dropdown
            ],
            outputs=[
                components["output_image"],
                components["save_status"]
            ],
            api_name="process_crop"
        )
    )
    
    return events

def bind_mask_events(components, lang_dropdown):
    events = []
    
    events.append(
        components["mask_refresh"].click(
            fn=lambda d: gr.update(
                choices=refresh_image_list(d),
                value=(refresh_image_list(d)[0] if refresh_image_list(d) else "")
            ),
            inputs=[components["mask_dir"]],
            outputs=[components["mask_dropdown"]],
            api_name="refresh_mask_list"
        )
    )
    
    events.append(
        components["image_refresh"].click(
            fn=lambda d: gr.update(
                choices=refresh_image_list(d),
                value=(refresh_image_list(d)[0] if refresh_image_list(d) else "")
            ),
            inputs=[components["image_dir"]],
            outputs=[components["image_dropdown"]],
            api_name="refresh_image_list"
        )
    )
    
    events.append(
        components["use_image"].change(
            fn=toggle_image_inputs,
            inputs=[components["use_image"]],
            outputs=[
                components["image_dir"],
                components["image_refresh"],
                components["image_dropdown"]
            ],
            api_name="toggle_image_inputs"
        )
    )
    
    events.append(
        components["process_btn"].click(
            fn=process_mask,
            inputs=[
                components["mask_dir"],
                components["mask_dropdown"],
                components["image_dir"],
                components["image_dropdown"],
                components["use_image"],
                components["out_dir"],
                components["out_filename"],
                lang_dropdown
            ],
            outputs=[
                components["result_image"],
                components["save_status"]
            ],
            api_name="process_mask"
        )
    )
    
    return events

def bind_language_change(lang_dropdown, title, resizer, cropper, mask):
    from ..utils import update_ui_language
    
    outputs = [title]
    
    outputs.extend([
        resizer["dir_text"],
        resizer["refresh_btn"],
        resizer["image_list"],
        resizer["input_image"],
        resizer["output_image"],
        resizer["aspect"]["target_size"],
        resizer["aspect"]["output_square"],
        resizer["aspect"]["margin"],
        resizer["aspect"]["process_btn"],
        resizer["custom"]["width"],
        resizer["custom"]["height"],
        resizer["custom"]["process_btn"],
        resizer["binary"]["apply"],
        resizer["binary"]["threshold"],
        resizer["blur"]["apply"],
        resizer["blur"]["radius"],
        resizer["out_dir"],
        resizer["out_filename"],
        resizer["save_status"]
    ])
    
    outputs.extend([
        cropper["dir_text"],
        cropper["image_list"],
        cropper["refresh_btn"],
        cropper["input_image"],
        cropper["output_image"],
        cropper["crop"]["top"],
        cropper["crop"]["bottom"],
        cropper["crop"]["left"],
        cropper["crop"]["right"],
        cropper["process"]["target_size"],
        cropper["process"]["output_square"],
        cropper["process"]["margin"],
        cropper["batch"]["process"],
        cropper["batch"]["folder"],
        cropper["out_dir"],
        cropper["out_filename"],
        cropper["process_btn"],
        cropper["save_status"]
    ])
    
    outputs.extend([
        mask["mask_dir"],
        mask["mask_refresh"],
        mask["mask_dropdown"],
        mask["use_image"],
        mask["image_dir"],
        mask["image_refresh"],
        mask["image_dropdown"],
        mask["out_dir"],
        mask["out_filename"],
        mask["process_btn"],
        mask["result_image"],
        mask["save_status"]
    ])
    
    event = lang_dropdown.change(
        fn=update_ui_language,
        inputs=[lang_dropdown],
        outputs=outputs,
        api_name="update_language"
    )
    
    return [event]