import os
import numpy as np
import cv2
from PIL import Image
from skimage import feature, filters
from ..utils import lang_labels

def process_edge_detection(input_dir, filename, algorithm, canny_low, canny_high, 
                          sigma, out_dir, out_filename, lang="English"):
    """
    Apply edge detection algorithms to an image:
    - Roberts, Sobel, Prewitt, Laplacian, LoG (Laplacian of Gaussian), and Canny
    - Allows customizing parameters for Canny and LoG algorithms
    """
    messages = lang_labels[lang]
    
    if not filename:
        return None, messages["no_image"]
    
    try:
        image_path = os.path.join(input_dir, filename)
        image = Image.open(image_path).convert("RGB")
        
        gray_image = np.array(image.convert("L"))
        
        result = None
        
        if algorithm == "Roberts":
            edges = filters.roberts(gray_image)
            result = (edges * 255).astype(np.uint8)
            
        elif algorithm == "Sobel":
            edges = filters.sobel(gray_image)
            result = (edges * 255).astype(np.uint8)
            
        elif algorithm == "Prewitt":
            edges = filters.prewitt(gray_image)
            result = (edges * 255).astype(np.uint8)
            
        elif algorithm == "Laplacian":
            result = cv2.Laplacian(gray_image, cv2.CV_64F)
            result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
        elif algorithm == "LoG":
            result = filters.gaussian(gray_image, sigma=sigma)
            result = filters.laplace(result)
            result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
        elif algorithm == "Canny":
            result = feature.canny(
                gray_image, 
                low_threshold=canny_low,
                high_threshold=canny_high
            )
            result = (result * 255).astype(np.uint8)
        
        output = Image.fromarray(result)
        
        status_message = ""
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            
            if not out_filename:
                base, ext = os.path.splitext(filename)
                out_filename = f"{base}_{algorithm.lower()}{ext}"
            
            output_path = os.path.join(out_dir, out_filename)
            output.save(output_path)
            status_message = messages["save_success"].format(output_path)
        
        return output, status_message
        
    except Exception as e:
        return None, messages["process_failed"].format(str(e))