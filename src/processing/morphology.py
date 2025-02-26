import os
import numpy as np
from PIL import Image
import cv2
from ..utils import lang_labels

def process_morphology(
    input_dir, filename, 
    apply_erosion, erosion_kernel, 
    apply_dilation, dilation_kernel,
    apply_opening, opening_kernel,
    apply_closing, closing_kernel,
    out_dir, out_filename, lang="English"
):
    messages = lang_labels[lang]
    if not filename:
        return None, messages["no_image"]
    
    input_path = os.path.join(input_dir, filename)
    try:
        image = Image.open(input_path)
        
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray_img = img_array
        
        _, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
        result = binary_img.copy()
        
        applied_operations = []
        
        if apply_erosion == "Yes":
            kernel_size = int(erosion_kernel)
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            result = cv2.erode(result, kernel, iterations=1)
            applied_operations.append("erosion")
        
        if apply_dilation == "Yes":
            kernel_size = int(dilation_kernel)
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            result = cv2.dilate(result, kernel, iterations=1)
            applied_operations.append("dilation")
        
        if apply_opening == "Yes":
            kernel_size = int(opening_kernel)
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
            applied_operations.append("opening")
        
        if apply_closing == "Yes":
            kernel_size = int(closing_kernel)
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
            applied_operations.append("closing")
        
        output_img = Image.fromarray(result)
        
        base, ext = os.path.splitext(filename)
        
        operations_str = "_".join(applied_operations) if applied_operations else "original"
        
        if not out_dir or out_dir.strip() == "":
            out_dir = os.path.join("output", base)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        
        if not out_filename:
            out_filename = f"{base}_morph_{operations_str}{ext}"
        out_path = os.path.join(out_dir, out_filename)
        
        output_img.save(out_path)
        return output_img, messages["save_success"].format(out_path)
    
    except Exception as e:
        return None, messages["process_failed"].format(str(e))