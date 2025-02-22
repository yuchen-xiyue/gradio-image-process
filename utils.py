import os
import numpy as np
from PIL import Image
import gradio as gr

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
    }
}

def refresh_file_list(directory):
    """
    Returns a list of image files in the specified directory (supports common image formats).
    """
    valid_extensions = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]
    if not os.path.exists(directory):
        return []
    files = [f for f in os.listdir(directory)
             if os.path.splitext(f)[1].lower() in valid_extensions]
    return files

def refresh_list(directory):
    """
    Refreshes the dropdown options based on the specified directory.
    Returns the updated dropdown value (first image if available).
    """
    files = refresh_file_list(directory)
    default_val = files[0] if files else None
    return gr.update(choices=files, value=default_val)

def refresh_image_list(dir_path):
    try:
        return [f for f in os.listdir(dir_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    except Exception as e:
        return []
    
            
def toggle_image_inputs(use_img):
    if use_img == "Yes":
        return gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
    else:
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)


def load_selected_image(directory, filename):
    """
    Loads the selected image from the given directory.
    """
    if not filename:
        return None
    path = os.path.join(directory, filename)
    try:
        return Image.open(path)
    except Exception as e:
        print(e)
        return None

def on_select_image(directory, filename):
    """
    Callback for when an image is selected from the dropdown.
    Returns the loaded image.
    """
    return load_selected_image(directory, filename)
