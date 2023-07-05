import fiftyone as fo

name = "my-dataset"
dataset_dir = "/mnt/extra/Datasets/aggregated_c/1lines"

# The splits to load
splits = ["train", "val"]

# Load the dataset, using tags to mark the samples in each split
dataset = fo.Dataset(name)
for split in splits:
    dataset.add_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.YOLOv5Dataset,
        split=split,
        tags=split,
)

# View summary info about the dataset
print(dataset)

# Print the first few samples in the dataset
print(dataset.head())