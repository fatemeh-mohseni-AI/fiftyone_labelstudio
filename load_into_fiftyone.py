import fiftyone as fo

# A name for the dataset
name = "confidential_line"

# The directory containing the dataset to import
dataset_dir = "/mnt/extra/Datasets/aggregated_c/1lines/split1/"
dataset_type = fo.types.YOLOv5Dataset  # for example

dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=dataset_type,
    name=name,
    )

session = fo.launch_app(dataset, address="0.0.0.0")
session.wait()

