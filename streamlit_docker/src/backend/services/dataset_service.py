import os
import cv2
from typing import Dict, List, Tuple
from ..config.config import get_config
from ..utils.dataset_utils import (
    get_split_paths,
    get_image_files,
    count_labels_in_file,
    analyze_image_blur,
    analyze_image_brightness,
    analyze_label_sizes
)

class DatasetAnalyzer:
    def __init__(self):
        self.config_manager = get_config()
        self.dataset_config = self.config_manager.get_active_dataset()
        if not self.dataset_config:
            raise ValueError("No active dataset selected")
        self.split_paths = get_split_paths(self.dataset_config.dataset_path)
        
    def count_labels_per_class(self) -> Tuple[Dict[str, int], int]:
        """Count total labels for each class across all splits"""
        class_counts = {cls: 0 for cls in self.dataset_config.classes}
        total_images = 0
        
        for split, paths in self.split_paths.items():
            image_files = get_image_files(paths)
            total_images += len(image_files)
            
            for img_path, label_path in image_files:
                counts = count_labels_in_file(label_path, len(self.dataset_config.classes), self.dataset_config.dataset_type)
                for class_id, count in counts.items():
                    class_counts[self.dataset_config.classes[class_id]] += count
        
        return class_counts, total_images
    
    def analyze_image_quality(self, split: str = 'train') -> List[Dict]:
        """Analyze image quality metrics for a split"""
        results = []
        
        if split not in self.split_paths:
            return results
            
        image_files = get_image_files(self.split_paths[split])
        
        for img_path, label_path in image_files:
            # Read image for dimensions
            img = cv2.imread(img_path)
            if img is None:
                print(f"Could not read image: {img_path}")
                continue
                
            height, width = img.shape[:2]
            
            # Analyze metrics
            blur_score = analyze_image_blur(img_path)
            brightness = analyze_image_brightness(img_path)
            label_sizes = analyze_label_sizes(label_path, self.dataset_config.dataset_type)
            
            results.append({
                'image': os.path.basename(img_path),
                'blur_score': blur_score,
                'brightness': brightness,
                'label_sizes': label_sizes,
                'avg_label_size': sum(label_sizes) / len(label_sizes) if label_sizes else 0
            })
            
        return results
        
    def get_dataset_stats(self) -> Dict:
        """Get overall dataset statistics"""
        stats = {
            'total_images': 0,
            'images_per_split': {},
            'total_labels': 0,
            'labels_per_class': {},
            'splits': list(self.split_paths.keys())
        }
        
        for split, paths in self.split_paths.items():
            image_files = get_image_files(paths)
            stats['images_per_split'][split] = len(image_files)
            stats['total_images'] += len(image_files)
            
            for _, label_path in image_files:
                counts = count_labels_in_file(label_path, len(self.dataset_config.classes), self.dataset_config.dataset_type)
                for class_id, count in counts.items():
                    class_name = self.dataset_config.classes[class_id]
                    if class_name not in stats['labels_per_class']:
                        stats['labels_per_class'][class_name] = 0
                    stats['labels_per_class'][class_name] += count
                    stats['total_labels'] += count
        
        return stats 