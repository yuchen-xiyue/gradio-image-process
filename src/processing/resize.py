import io
import os
import cairosvg
from PIL import Image, ImageFilter
from ..utils import lang_labels

def load_image(input_path, lang="English"):
    """Helper function to load both regular images and SVGs"""
    messages = lang_labels[lang]
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(messages["file_not_found"])
        
    if input_path.lower().endswith('.svg'):
        try:
            # Use cairosvg instead of svglib/reportlab
            png_data = cairosvg.svg2png(
                url=input_path,
                output_height=1024,  # Reasonable default size
                output_width=1024,   # Will maintain aspect ratio
                scale=2.0,           # Better quality
                background_color='white'  # Set white background for SVG
            )
            image = Image.open(io.BytesIO(png_data))
        except Exception as e:
            raise ValueError(f"{messages['svg_convert_failed']}: {str(e)}")
    else:
        try:
            image = Image.open(input_path)
            image.verify()  # Verify image integrity
            image = Image.open(input_path)  # Reopen after verify
        except Exception as e:
            raise ValueError(f"{messages['image_load_failed']}: {str(e)}")
    
    # Convert to RGB mode if necessary
    try:
        if image.mode != 'RGB':
            image = image.convert('RGB')
    except Exception as e:
        raise ValueError(f"{messages['convert_failed']}: {str(e)}")
    
    return image

def process_image_aspect(input_dir, filename, target_size, output_square,
                         out_dir, out_filename, apply_binary, binary_threshold, margin, apply_blur, blur_radius, lang="English"):
    """
    Processes the image in Aspect Rescale mode:
      - Rescales the image so that its long side equals target_size.
      - If output_square is True, pads the image to output a square.
      - If apply_binary is True, applies binary conversion using the binary_threshold.
    
    Saves the processed image to the specified output folder. If no output folder is provided,
    it automatically saves to "output/{input_filename_without_ext}".
    
    Returns the processed image and a status message.
    """
    messages = lang_labels[lang]
    if not filename:
        return None, messages["no_image"]
    input_path = os.path.join(input_dir, filename)
    try:
        image = load_image(input_path, lang)
    except Exception as e:
        return None, messages["open_failed"].format(str(e))
    
    effective_target_size = target_size - (2 * margin)

    # Calculate scale factor for aspect rescaling
    factor = effective_target_size / max(image.width, image.height)
    new_width = int(image.width * factor)
    new_height = int(image.height * factor)
    resized_img = image.resize((new_width, new_height), Image.LANCZOS)
    
    if output_square:
        # Create a square white background and paste the resized image centered
        output_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
        offset_x = (target_size - new_width) // 2
        offset_y = (target_size - new_height) // 2
    else:
        output_img = Image.new("RGB", (new_width + 2*margin, new_height + 2*margin), (255, 255, 255))
        offset_x = margin
        offset_y = margin
    
    output_img.paste(resized_img, (offset_x, offset_y))
    mode_str = "aspect_square" if output_square else "aspect"

    
    # Apply binary conversion if enabled (convert UI threshold 0-1 to 0-255)
    if apply_binary:
        gray_img = output_img.convert("L")
        threshold = binary_threshold * 255
        binary_img = gray_img.point(lambda p: 255 if p > threshold else 0, mode="1")
        output_img = binary_img.convert("RGB")
        mode_str += "_binary"
    
    # Apply Gaussian blur after binary processing if requested
    if apply_blur and isinstance(blur_radius, (int, float)):
        output_img = output_img.filter(ImageFilter.GaussianBlur(radius=float(blur_radius)))
        mode_str += "_blur"
        
    # Automatically structure the output directory if not specified or default is used
    base, ext = os.path.splitext(filename)
    if not out_dir or out_dir.strip() == "" or out_dir.strip() == messages["default_output"]:
        out_dir = os.path.join(messages["default_output"], base)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    
    # Auto-generate output filename if not provided
    if not out_filename:
        if filename.lower().endswith('.svg'):
            ext = '.png'  # Force PNG output for SVG inputs
        out_filename = f"{base}_{mode_str}{ext}"
    out_path = os.path.join(out_dir, out_filename)
    
    try:
        output_img.save(out_path)
        status = messages["save_success"].format(out_path)
    except Exception as e:
        status = messages["save_failed"].format(str(e))
    
    return output_img, status

def process_image_custom(input_dir, filename, target_width, target_height,
                         out_dir, out_filename, apply_binary, binary_threshold, apply_blur, blur_radius, lang):
    """
    Processes the image in Custom Resize mode:
      - Directly resizes the image to target_width and target_height.
      - If apply_binary is True, applies binary conversion using the binary_threshold.
    
    Saves the processed image to the specified output folder. If no output folder is provided,
    it automatically saves to "output/{input_filename_without_ext}".
    
    Returns the processed image and a status message.
    """
    messages = lang_labels[lang]
    if not filename:
        return None, messages["no_image"]
    input_path = os.path.join(input_dir, filename)
    try:
        image = load_image(input_path, lang)
    except Exception as e:
        return None, messages["open_failed"].format(str(e))
    
    output_img = image.resize((target_width, target_height), Image.LANCZOS)
    mode_str = "custom"
    
    if apply_binary:
        gray_img = output_img.convert("L")
        threshold = binary_threshold * 255
        binary_img = gray_img.point(lambda p: 255 if p > threshold else 0, mode="1")
        output_img = binary_img.convert("RGB")
        mode_str += "_binary"
    
    # Apply Gaussian blur after binary processing if requested
    if apply_blur and isinstance(blur_radius, (int, float)):
        output_img = output_img.filter(ImageFilter.GaussianBlur(radius=float(blur_radius)))
        mode_str += "_blur"

    base, ext = os.path.splitext(filename)
    if not out_dir or out_dir.strip() == "" or out_dir.strip() == messages["default_output"]:
        out_dir = os.path.join(messages["default_output"], base)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    
    if not out_filename:
        if filename.lower().endswith('.svg'):
            ext = '.png'  # Force PNG output for SVG inputs
        out_filename = f"{base}_{mode_str}{ext}"
    out_path = os.path.join(out_dir, out_filename)
    
    try:
        output_img.save(out_path)
        status = messages["save_success"].format(out_path)
    except Exception as e:
        status = messages["save_failed"].format(str(e))
    
    return output_img, status
