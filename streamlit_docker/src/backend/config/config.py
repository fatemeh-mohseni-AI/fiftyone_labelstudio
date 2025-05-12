import os
import yaml
from typing import List, Dict

class DatasetConfig:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.yaml_path = os.path.join(dataset_path, "dataset.yaml")
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

# Global config instance
dataset_config = None

def init_config(dataset_path: str = "/dataset1"):
    """Initialize global configuration"""
    global dataset_config
    dataset_config = DatasetConfig(dataset_path)
    return dataset_config

def get_config() -> DatasetConfig:
    """Get global configuration instance"""
    if dataset_config is None:
        raise RuntimeError("Configuration not initialized. Call init_config first.")
    return dataset_config 