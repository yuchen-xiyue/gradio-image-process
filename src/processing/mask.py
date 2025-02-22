import os
from PIL import Image, ImageFilter
from ..utils import lang_labels
import numpy as np

def process_mask(dir_mask, mask_file, dir_image, image_file, use_img,
                out_dir, out_filename, lang):
    
    messages = lang_labels[lang]
    if not mask_file:
        return None, messages["no_image"]

    mask_path = os.path.join(dir_mask, mask_file)
    mask = Image.open(mask_path).convert("L")
    canvas_width, canvas_height = mask.size
    background = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
    mask_binary = mask.point(lambda p: 255 if p > 128 else 0)
    if use_img == "Yes":
        image_path = os.path.join(dir_image, image_file)
        img_input = Image.open(image_path).convert("RGB").resize((canvas_width, canvas_height))
        output = Image.composite(img_input, background, mask_binary)
    else:
        black_image = Image.new("RGB", (canvas_width, canvas_height), (0, 0, 0))
        output = Image.composite(black_image, background, mask_binary)
    
    base, ext = os.path.splitext(mask_file)
    if not out_dir or out_dir.strip() == "" or out_dir.strip() == "output":
        out_dir = os.path.join("output", base)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    mode_str = "stroke"
    if not out_filename:
        out_filename = f"{base}_{mode_str}{ext}"
    out_path = os.path.join(out_dir, out_filename)
    
    try:
        output.save(out_path)
        status = messages["save_success"].format(out_path)
    except Exception as e:
        status = messages["save_failed"].format(str(e))

    return np.array(output) / 255.0, status
