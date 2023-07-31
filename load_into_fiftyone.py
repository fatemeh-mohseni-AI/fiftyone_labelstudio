import fiftyone as fo

# A name for the dataset
name = "check"

# The directory containing the dataset to import
dataset_dir = "/mnt/extra/Datasets/v4_aggregated/labeled_line"
dataset_type = fo.types.YOLOv5Dataset  # for example


dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=dataset_type,
    name=name,
    tags=["ground_truth"],
    )

session = fo.launch_app(dataset, address="0.0.0.0", port=4545)
session.wait()

