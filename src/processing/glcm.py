import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.feature import graycomatrix, graycoprops
import cv2
from ..utils import lang_labels
import io

def process_glcm_features(
    input_dir, filename,
    distance, angles, levels,
    symmetric, normalize,
    include_contrast, include_dissimilarity,
    include_homogeneity, include_energy,
    include_correlation, include_asm,
    lang="English"
):
    messages = lang_labels[lang]
    
    if not filename:
        return None, [["No image selected", ""]], {}
    
    try:
        input_path = os.path.join(input_dir, filename)
        image = Image.open(input_path)
        
        if image.mode != 'L':
            image = image.convert('L')
        
        img_array = np.array(image)
        
        window_size = 16  
        step_size = 8     
        
        height, width = img_array.shape
        
        feature_maps = {}
        if include_contrast:
            feature_maps["Contrast"] = np.zeros((height, width), dtype=np.float32)
        if include_dissimilarity:
            feature_maps["Dissimilarity"] = np.zeros((height, width), dtype=np.float32)
        if include_homogeneity:
            feature_maps["Homogeneity"] = np.zeros((height, width), dtype=np.float32)
        if include_energy:
            feature_maps["Energy"] = np.zeros((height, width), dtype=np.float32)
        if include_correlation:
            feature_maps["Correlation"] = np.zeros((height, width), dtype=np.float32)
        if include_asm:
            feature_maps["ASM"] = np.zeros((height, width), dtype=np.float32)
        
        angle_map = {
            "0°": 0,
            "45°": np.pi/4,
            "90°": np.pi/2,
            "135°": 3*np.pi/4
        }
        angles_rad = [angle_map[a] for a in angles]
        
        for y in range(0, height - window_size + 1, step_size):
            for x in range(0, width - window_size + 1, step_size):
                window = img_array[y:y+window_size, x:x+window_size]
                
                max_value = levels - 1
                bins = np.linspace(0, 255, levels)
                rescaled_window = np.digitize(window, bins) - 1
                
                glcm = graycomatrix(
                    rescaled_window, 
                    distances=[distance], 
                    angles=angles_rad,
                    levels=levels,
                    symmetric=symmetric,
                    normed=normalize
                )
                
                for feature_name in feature_maps.keys():
                    if feature_name == "ASM":
                        prop_name = "ASM"
                    else:
                        prop_name = feature_name.lower()
                    
                    value = np.mean(graycoprops(glcm, prop_name)[0])
                    
                    for wy in range(window_size):
                        for wx in range(window_size):
                            py, px = y + wy, x + wx
                            if py < height and px < width:
                                if feature_maps[feature_name][py, px] != 0:
                                    feature_maps[feature_name][py, px] = (feature_maps[feature_name][py, px] + value) / 2
                                else:
                                    feature_maps[feature_name][py, px] = value
        
        for feature_name, feature_map in feature_maps.items():
            if np.max(feature_map) > np.min(feature_map):  
                feature_maps[feature_name] = (feature_map - np.min(feature_map)) / (np.max(feature_map) - np.min(feature_map))
        
        feature_table = []
        for feature_name, feature_map in feature_maps.items():
            mean_value = np.mean(feature_map)
            std_value = np.std(feature_map)
            min_value = np.min(feature_map)
            max_value = np.max(feature_map)
            feature_table.append([
                feature_name, 
                f"{mean_value:.5f} ± {std_value:.5f} (min: {min_value:.5f}, max: {max_value:.5f})"
            ])
        
        if feature_maps:
            n_features = len(feature_maps)
            n_cols = min(n_features, 3)  
            n_rows = (n_features + n_cols - 1) // n_cols  
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4*n_rows))
            if n_features == 1:  
                axes = np.array([axes])
            axes = axes.flatten()
            
            for i, (feature_name, feature_map) in enumerate(feature_maps.items()):
                if i < len(axes):
                    im = axes[i].imshow(feature_map, cmap='viridis')
                    axes[i].set_title(feature_name)
                    axes[i].axis('off')
                    fig.colorbar(im, ax=axes[i])
            
            for i in range(n_features, len(axes)):
                axes[i].axis('off')
                
            plt.tight_layout()
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150)
            buf.seek(0)
            feature_img = np.array(Image.open(buf))
            plt.close(fig)
            
            return feature_img, feature_table, feature_maps
        else:
            plt.figure(figsize=(8, 6))
            plt.text(0.5, 0.5, "No features selected", 
                     ha='center', va='center', fontsize=14)
            plt.axis('off')
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            empty_img = np.array(Image.open(buf))
            plt.close()
            
            return empty_img, [["No features selected", ""]], {}
    
    except Exception as e:
        # 错误处理
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, f"Error: {str(e)}", 
                 ha='center', va='center', fontsize=14, color='red')
        plt.axis('off')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        error_img = np.array(Image.open(buf))
        plt.close()
        
        return error_img, [["Error", str(e)]], {}