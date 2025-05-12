import os
import yaml
from typing import List, Dict, Optional
from enum import Enum

class DatasetType(Enum):
    BBOX = "bbox"
    SEGMENT = "segment"

class DatasetConfig:
    def __init__(self, dataset_path: str, dataset_type: Optional[DatasetType] = None):
        self.dataset_path = dataset_path
        self.yaml_path = os.path.join(dataset_path, "dataset.yaml")
        self.dataset_type = dataset_type
        self._load_config()

    def _load_config(self):
        """Load configuration from dataset.yaml"""
        if not os.path.exists(self.yaml_path):
            raise FileNotFoundError(f"Dataset configuration file not found at {self.yaml_path}")
        
        with open(self.yaml_path, 'r') as f:
            config = yaml.safe_load(f)
            
        self.train_path = os.path.join(self.dataset_path, config.get('train', 'train'))
        self.val_path = os.path.join(self.dataset_path, config.get('val', 'valid'))
        self.test_path = os.path.join(self.dataset_path, config.get('test', 'test'))
        self.classes = config.get('names', [])
        self.nc = len(self.classes)

        # Try to auto-detect dataset type if not specified
        if self.dataset_type is None:
            self.dataset_type = self._detect_dataset_type()

    def _detect_dataset_type(self) -> DatasetType:
        """Try to detect if dataset is bbox or segment based on label format"""
        # Check first label file we can find
        for split_path in [self.train_path, self.val_path, self.test_path]:
            labels_dir = os.path.join(split_path, 'labels')
            if os.path.exists(labels_dir):
                for label_file in os.listdir(labels_dir):
                    if label_file.endswith('.txt'):
                        with open(os.path.join(labels_dir, label_file), 'r') as f:
                            first_line = f.readline().strip()
                            if first_line:
                                parts = first_line.split()
                                # Segment format has more than 5 values (class + points)
                                return DatasetType.SEGMENT if len(parts) > 5 else DatasetType.BBOX
        return DatasetType.BBOX  # Default to BBOX if can't detect

    @property
    def splits(self) -> List[str]:
        """Return list of available splits"""
        return ['train', 'val', 'test']

    @property
    def split_paths(self) -> Dict[str, str]:
        """Return dictionary of split paths"""
        return {
            'train': self.train_path,
            'val': self.val_path,
            'test': self.test_path
        }

class ConfigManager:
    def __init__(self):
        self.datasets: Dict[str, DatasetConfig] = {}
        self.active_dataset: Optional[str] = None

    def discover_datasets(self):
        """Discover all mounted datasets in the container"""
        # Look for mounted volumes that contain dataset.yaml
        for root, dirs, files in os.walk('/'):
            if 'dataset.yaml' in files:
                dataset_name = os.path.basename(root)
                try:
                    self.datasets[dataset_name] = DatasetConfig(root)
                    print(f"Discovered dataset: {dataset_name} at {root}")
                except Exception as e:
                    print(f"Error loading dataset at {root}: {e}")

    def set_dataset_type(self, dataset_name: str, dataset_type: DatasetType):
        """Set the type of a specific dataset"""
        if dataset_name in self.datasets:
            self.datasets[dataset_name].dataset_type = dataset_type

    def get_dataset(self, dataset_name: str) -> Optional[DatasetConfig]:
        """Get configuration for a specific dataset"""
        return self.datasets.get(dataset_name)

    def set_active_dataset(self, dataset_name: str):
        """Set the active dataset"""
        if dataset_name in self.datasets:
            self.active_dataset = dataset_name
        else:
            raise ValueError(f"Dataset {dataset_name} not found")

    def get_active_dataset(self) -> Optional[DatasetConfig]:
        """Get the active dataset configuration"""
        if self.active_dataset:
            return self.datasets[self.active_dataset]
        return None

# Global config manager instance
config_manager = None

def init_config():
    """Initialize global configuration manager"""
    global config_manager
    config_manager = ConfigManager()
    config_manager.discover_datasets()
    return config_manager

def get_config() -> ConfigManager:
    """Get global configuration manager instance"""
    if config_manager is None:
        raise RuntimeError("Configuration not initialized. Call init_config first.")
    return config_manager 