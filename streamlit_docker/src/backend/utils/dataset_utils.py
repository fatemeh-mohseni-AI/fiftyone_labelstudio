import os
import glob
import cv2
import numpy as np
from typing import Dict, Tuple, List
from ..config.config import DatasetType

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

def parse_label_line(line: str, dataset_type: DatasetType) -> Tuple[int, List[float]]:
    """Parse a single line from a label file based on dataset type"""
    parts = line.strip().split()
    if len(parts) < 5:
        return -1, []
        
    class_id = int(parts[0])
    
    if dataset_type == DatasetType.BBOX:
        # BBOX format: class x y w h
        coords = [float(x) for x in parts[1:5]]
    else:
        # Segment format: class x1 y1 x2 y2 ...
        coords = [float(x) for x in parts[1:]]
        
    return class_id, coords

def count_labels_in_file(label_path: str, num_classes: int, dataset_type: DatasetType) -> Dict[int, int]:
    """Count labels in a single label file"""
    counts = {i: 0 for i in range(num_classes)}
    try:
        with open(label_path, 'r') as f:
            for line in f:
                class_id, _ = parse_label_line(line, dataset_type)
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

def calculate_bbox_area(coords: List[float]) -> float:
    """Calculate area for bbox coordinates"""
    if len(coords) >= 4:
        return coords[2] * coords[3]  # w * h
    return 0.0

def calculate_segment_area(coords: List[float]) -> float:
    """Calculate area for segment coordinates"""
    if len(coords) < 4 or len(coords) % 2 != 0:
        return 0.0
        
    # Convert coordinates to points
    points = np.array([(coords[i], coords[i+1]) for i in range(0, len(coords), 2)])
    
    # Calculate area using shoelace formula
    x = points[:, 0]
    y = points[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def analyze_label_sizes(label_path: str, dataset_type: DatasetType) -> List[float]:
    """Analyze relative sizes of labels in an image"""
    sizes = []
    try:
        with open(label_path, 'r') as f:
            for line in f:
                _, coords = parse_label_line(line, dataset_type)
                if coords:
                    if dataset_type == DatasetType.BBOX:
                        area = calculate_bbox_area(coords)
                    else:
                        area = calculate_segment_area(coords)
                    if area > 0:
                        sizes.append(area)
    except Exception as e:
        print(f"Error analyzing label sizes in {label_path}: {e}")
    return sizes 