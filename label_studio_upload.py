import fiftyone as fo

# Step 1: Load your data into FiftyOne

dataset_name = "dataset"
dataset_dir = "/home/fatemeh/Desktop/split1/1"

# Load the dataset, using tags to mark the samples in each split
if dataset_name in fo.list_datasets():
        dataset = fo.load_dataset(dataset_name)
else:
        dataset = fo.Dataset.from_dir(
                dataset_dir=dataset_dir,
                dataset_type=fo.types.YOLOv5Dataset,
                tags=dataset_name,
                dataset_name=dataset_name
        )
dataset.persistent = True
view = dataset.view()

# A unique identifier for this run
anno_key = "change_this_line_12345"

label_schema = {
    "new_ground_truth": {
        "type": "detections",
        "classes": dataset.distinct("ground_truth.detections.label"),
    },
}
view.annotate(
    anno_key,
    project_name="fiftyone_test",
    backend="labelstudio",
    label_field="ground_truth",
    url="http://localhost:8080",
    api_key="94b10acd4d3af0f7026cde0ab8a8fb8a60a3a6ef",  # check READ.ME file
    launch_editor=True,
    timeout=1000
)
print(dataset.get_annotation_info(anno_key))