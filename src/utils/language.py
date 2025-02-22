# Language labels dictionary
lang_labels = {
    "English": {
        "title": "Image Processing Tool",
        "input_folder": "Input Image Folder",
        "refresh_list": "Refresh Image List",
        "select_image": "Select Image",
        "input_image": "Input Image",
        "output_image": "Output Image",
        "aspect_tab": "Aspect Rescale",
        "custom_tab": "Custom Resize",
        "target_size": "Target size for long side (pixels)",
        "output_square": "Output Square (Padding)",
        "process_aspect": "Process Image (Aspect)",
        "target_width": "Target Width (pixels)",
        "target_height": "Target Height (pixels)",
        "process_custom": "Process Image (Custom)",
        "apply_binary": "Apply Binary",
        "binary_threshold": "Binary Threshold (0-1)",
        "output_folder": "Output Folder (optional)",
        "output_filename": "Output Filename (optional)",
        "save_status": "Save Status",
        "language": "Language",
        "no_image": "No image selected",
        "open_failed": "Failed to open image: {}",
        "save_success": "Save successful: {}",
        "save_failed": "Save failed: {}",
        "default_output": "output",
        "image_resizer": "Image Resizer",
        "mask_renderer": "Mask Renderer",
        "mask_dir": "Mask File Directory",
        "mask_refresh": "Refresh Mask List",
        "mask_select": "Select Mask File",
        "use_image": "Use Image Input?",
        "image_dir": "Image File Directory",
        "image_refresh": "Refresh Image List",
        "process_mask": "Render Mask",
        "rendered_mask": "Rendered Mask",
        "margin": "Margin (pixels)",
        "apply_blur": "Apply Gaussian Blur",
        "blur_radius": "Blur Radius (1-10)",
        "image_cropper": "Image Cropper",
        "crop_top": "Top Margin",
        "crop_bottom": "Bottom Margin",
        "crop_left": "Left Margin",
        "crop_right": "Right Margin",
        "target_crop_size": "Target Size",
        "crop_square": "Output Square",
        "crop_margins": "Output Margins",
        "batch_process": "Batch Process",
        "process_crop": "Process Crop",
        "batch_folder": "Batch Input Folder",
    },
    "中文": {
        "title": "图片处理工具",
        "input_folder": "输入图片文件夹",
        "refresh_list": "刷新图片列表",
        "select_image": "选择图片",
        "input_image": "输入图片",
        "output_image": "输出图片",
        "aspect_tab": "等比缩放",
        "custom_tab": "非等比缩放",
        "target_size": "长边目标尺寸 (像素)",
        "output_square": "输出正方形 (填充)",
        "process_aspect": "处理图片 (等比)",
        "target_width": "目标宽度 (像素)",
        "target_height": "目标高度 (像素)",
        "process_custom": "处理图片 (非等比)",
        "apply_binary": "应用二值化",
        "binary_threshold": "二值化阈值 (0-1)",
        "output_folder": "输出文件夹（可选）",
        "output_filename": "输出文件名（可选）",
        "save_status": "保存状态",
        "language": "语言",
        "no_image": "未选择图片",
        "open_failed": "打开图片失败：{}",
        "save_success": "保存成功：{}",
        "save_failed": "保存失败：{}",
        "default_output": "output",
        "image_resizer": "图像缩放器",
        "mask_renderer": "遮罩生成器",
        "mask_dir": "遮罩文件目录",
        "mask_refresh": "刷新遮罩列表",
        "mask_select": "选择遮罩文件",
        "use_image": "使用图片输入？",
        "image_dir": "图片文件目录",
        "image_refresh": "刷新图片列表",
        "process_mask": "生成遮罩",
        "rendered_mask": "生成的遮罩",
        "margin": "边距 (像素)",
        "apply_blur": "应用高斯模糊",
        "blur_radius": "模糊半径 (1-10)",
        "image_cropper": "图片裁剪",
        "crop_top": "上边距",
        "crop_bottom": "下边距",
        "crop_left": "左边距",
        "crop_right": "右边距",
        "target_crop_size": "目标尺寸",
        "crop_square": "输出正方形",
        "crop_margins": "输出边距",
        "batch_process": "批量处理",
        "process_crop": "处理裁剪",
        "batch_folder": "批量输入文件夹",
    }
}

import gradio as gr
# ---------------------------
# Callback to Update UI Labels Dynamically
# ---------------------------
def update_ui_language(lang):
    """
    When the language selection changes, update the labels of various UI components.
    Returns updated values for the title markdown and for components that support update.
    """
    messages = lang_labels[lang]
    return (
        gr.update(value=f"# {messages['title']}"),                # title_markdown
        gr.update(label=messages["input_folder"]),                # dir_text
        gr.update(value=messages["refresh_list"]),                # refresh_btn
        gr.update(label=messages["select_image"]),                # image_list
        gr.update(label=messages["input_image"]),                 # input_image
        gr.update(label=messages["output_image"]),                # output_image
        gr.update(label=messages["target_size"]),                 # target_size_slider
        gr.update(label=messages["output_square"]),               # output_square_checkbox
        gr.update(label=messages["margin"]),                      # margin_slider
        gr.update(value=messages["process_aspect"]),              # process_aspect_btn
        gr.update(label=messages["target_width"]),                # target_width_slider
        gr.update(label=messages["target_height"]),               # target_height_slider
        gr.update(value=messages["process_custom"]),              # process_custom_btn
        gr.update(label=messages["apply_binary"]),                # apply_binary_checkbox
        gr.update(label=messages["binary_threshold"]),            # binary_threshold_slider
        gr.update(label=messages["apply_blur"]),                  # apply_blur_checkbox
        gr.update(label=messages["blur_radius"]),                 # blur_radius_slider
        gr.update(label=messages["output_folder"]),               # out_dir_text
        gr.update(label=messages["output_filename"]),             # out_filename_text
        gr.update(label=messages["save_status"]),                 # save_status
        gr.update(label=messages["mask_dir"]),                    # mask_dir_input
        gr.update(value=messages["mask_refresh"]),                # mask_refresh_button
        gr.update(label=messages["mask_select"]),                 # mask_dropdown
        gr.update(label=messages["use_image"]),                   # use_image_radio
        gr.update(label=messages["image_dir"]),                   # image_dir_input
        gr.update(value=messages["image_refresh"]),               # image_refresh_button
        gr.update(label=messages["select_image"]),                # image_dropdown
        gr.update(label=messages["output_folder"]),               # out_dir_text_mask
        gr.update(label=messages["output_filename"]),             # out_filename_text_mask
        gr.update(value=messages["process_mask"]),                # process_mask_button
        
        gr.update(label=messages["input_folder"]),                # dir_text_crop
        gr.update(label=messages["select_image"]),                # image_list_crop
        gr.update(value=messages["refresh_list"]),                # refresh_btn_crop
        gr.update(label=messages["input_image"]),                 # input_image_crop
        gr.update(label=messages["output_image"]),                # output_image_crop
        gr.update(label=messages["crop_top"]),                    # crop_top
        gr.update(label=messages["crop_bottom"]),                 # crop_bottom
        gr.update(label=messages["crop_left"]),                   # crop_left
        gr.update(label=messages["crop_right"]),                  # crop_right
        gr.update(label=messages["target_crop_size"]),            # target_size_crop
        gr.update(label=messages["crop_square"]),                 # output_square_crop
        gr.update(label=messages["crop_margins"]),                # margin_crop
        gr.update(label=messages["batch_process"]),               # batch_process
        gr.update(label=messages["batch_folder"]),                # batch_folder
        gr.update(label=messages["output_folder"]),               # out_dir_crop
        gr.update(label=messages["output_filename"]),             # out_filename_crop
        gr.update(value=messages["process_crop"]),                # process_crop_btn
        gr.update(label=messages["save_status"])                  # save_status_crop
    )