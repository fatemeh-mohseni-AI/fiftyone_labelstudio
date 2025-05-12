import os
import glob
import cv2
import numpy as np
from typing import Dict, Tuple, List

def get_split_paths(dataset_root: str) -> Dict[str, Dict[str, str]]:
    """Get paths for images and labels directories for each split"""
    splits = ['train', 'test', 'valid']
    paths = {}
    
    for split in splits:
        split_dir = os.path.join(dataset_root, split)
        if os.path.exists(split_dir):
            paths[split] = {
                'images': os.path.join(split_dir, 'images'),
                'labels': os.path.join(split_dir, 'labels')
            }
    
    return paths

def get_image_files(split_path: Dict[str, str]) -> List[Tuple[str, str]]:
    """
    Get all image files and their corresponding label files in a split
    Returns: List of tuples (image_path, label_path)
    """
    image_files = []
    images_dir = split_path['images']
    labels_dir = split_path['labels']
    
    if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
        return image_files
    
    # Get all image files
    for ext in ['.jpg', '.jpeg', '.png']:
        for img_path in glob.glob(os.path.join(images_dir, f"*{ext}")):
            img_name = os.path.basename(img_path)
            base_name = os.path.splitext(img_name)[0]
            label_path = os.path.join(labels_dir, f"{base_name}.txt")
            
            # Only include if both image and label exist
            if os.path.exists(label_path):
                image_files.append((img_path, label_path))
    
    return sorted(image_files)

def count_labels_in_file(label_path: str, num_classes: int) -> Dict[int, int]:
    """Count labels in a single label file"""
    counts = {i: 0 for i in range(num_classes)}
    try:
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:  # YOLO format requires at least 5 values (class x y w h)
                    class_id = int(parts[0])
                    if 0 <= class_id < num_classes:
                        counts[class_id] += 1
    except Exception as e:
        print(f"Error reading label file {label_path}: {e}")
    return counts

def analyze_image_blur(image_path: str) -> float:
    """Calculate blur score for an image (lower means more blurry)"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not read image: {image_path}")
            return 0.0
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()
    except Exception as e:
        print(f"Error analyzing blur in {image_path}: {e}")
        return 0.0

def analyze_image_brightness(image_path: str) -> float:
    """Calculate average brightness of an image"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not read image: {image_path}")
            return 0.0
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return hsv[:, :, 2].mean()
    except Exception as e:
        print(f"Error analyzing brightness in {image_path}: {e}")
        return 0.0

def analyze_label_sizes(label_path: str, image_size: Tuple[int, int]) -> List[float]:
    """Analyze relative sizes of labels in an image"""
    sizes = []
    try:
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:  # YOLO format: class x y w h
                    w = float(parts[3])  # width is already normalized
                    h = float(parts[4])  # height is already normalized
                    area = w * h  # This is already relative area since YOLO coordinates are normalized
                    sizes.append(area)
    except Exception as e:
        print(f"Error analyzing label sizes in {label_path}: {e}")
    return sizes 