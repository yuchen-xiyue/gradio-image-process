import os
import io
import numpy as np
from PIL import Image
import gradio as gr
import cairosvg



def refresh_file_list(directory):
    """
    Returns a list of image files in the specified directory (supports common image formats).
    """
    valid_extensions = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".svg", ".tif", ".tiff"]
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
        return [f for f in os.listdir(dir_path) if f.lower().endswith(
            (".png", ".jpg", ".jpeg", ".svg", ".tif", ".tiff"))]
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
    Supports regular image formats and SVG files.
    """
    if not filename:
        return None
    
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        return None

    try:
        # Handle SVG files
        if filename.lower().endswith('.svg'):
            # Convert SVG to PNG using cairosvg
            png_data = cairosvg.svg2png(
                url=path,
                output_height=1024,  # Default size
                output_width=1024,   # Will maintain aspect ratio
                scale=2.0,           # Better quality
                background_color='white'  # Set white background for SVG
            )
            image = Image.open(io.BytesIO(png_data))
        else:
            # Handle regular image formats
            image = Image.open(path)
            image.verify()  # Verify image integrity
            image = Image.open(path)  # Reopen after verify
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        return image
        
    except Exception as e:
        print(f"Error loading image {filename}: {str(e)}")
        return None

def on_select_image(directory, filename):
    """
    Callback for when an image is selected from the dropdown.
    Returns the loaded image.
    """
    return load_selected_image(directory, filename)
