import os
import io
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from ..utils import lang_labels
import numpy as np

def process_image_crop(input_dir, filename, top, bottom, left, right, target_size, 
                      output_square, margin, batch_process, batch_folder, out_dir, 
                      out_filename, lang="English"):
    """
    Crop image based on margins and resize to target size:
    - Crop image using specified margins
    - Resize maintaining aspect ratio to target size
    - Optionally make output square with padding
    - Add output margins if specified
    - Support batch processing
    """
    messages = lang_labels[lang]
    
    if batch_process:
        # Process all images in batch folder
        results = []
        for img_file in os.listdir(batch_folder):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.svg', '.tif')):
                result = process_single_crop(batch_folder, img_file, top, bottom, left, right,
                                          target_size, output_square, margin, out_dir, None, lang)
                results.append(result)
        return None, "\n".join([r[1] for r in results])
    else:
        # Process single image
        return process_single_crop(input_dir, filename, top, bottom, left, right,
                                 target_size, output_square, margin, out_dir, out_filename, lang)


def process_single_crop(input_dir, filename, top, bottom, left, right, target_size, 
                       output_square, margin, out_dir, out_filename, lang):
    """Process a single image for cropping"""
    if not filename:
        return None, lang_labels[lang]["no_image"]
    
    input_path = os.path.join(input_dir, filename)
    try:
        # Check if file is SVG
        if filename.lower().endswith('.svg'):
            # Convert SVG to PNG using svglib
            drawing = svg2rlg(input_path)
            # Convert to PIL Image
            png_data = renderPM.drawToString(drawing, fmt='PNG')
            image = Image.open(io.BytesIO(png_data))
        else:
            image = Image.open(input_path)
        
        # Convert to RGB mode if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Crop image
        width, height = image.size
        crop_box = (left, top, width - right, height - bottom)
        cropped = image.crop(crop_box)
        
        # Calculate resize factor
        crop_width, crop_height = cropped.size
        factor = target_size / max(crop_width, crop_height)
        new_width = int(crop_width * factor)
        new_height = int(crop_height * factor)
        
        # Resize maintaining aspect ratio
        resized = cropped.resize((new_width, new_height), Image.LANCZOS)
        
        # Handle square output if requested
        if output_square:
            size = target_size + (2 * margin)
            output_img = Image.new("RGB", (size, size), (255, 255, 255))
            offset_x = (size - new_width) // 2
            offset_y = (size - new_height) // 2
        else:
            output_img = Image.new("RGB", (new_width + 2*margin, new_height + 2*margin), 
                                 (255, 255, 255))
            offset_x = margin
            offset_y = margin
        
        output_img.paste(resized, (offset_x, offset_y))
        
        # Save the processed image
        base, ext = os.path.splitext(filename)
        mode_str = "crop"
        if output_square:
            mode_str += "_square"
        
        if not out_dir or out_dir.strip() == "":
            out_dir = "output"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
            
        if not out_filename:
            out_filename = f"{base}_{mode_str}{ext}"
        out_path = os.path.join(out_dir, out_filename)
        
        output_img.save(out_path)
        return output_img, lang_labels[lang]["save_success"].format(out_path)
        
    except Exception as e:
        return None, lang_labels[lang]["process_failed"].format(str(e))