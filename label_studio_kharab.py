import fiftyone as fo
import fiftyone.zoo as foz
from fiftyone import ViewField as F

# Step 1: Load your data into FiftyOne


dataset_name = "asdfafs"
#dataset_dir = "/mnt/extra/Datasets/v1/3_RoboFlow_all_in_v2/line_pot/1"
dataset_dir = "/home/fatemeh/Desktop/split1/1"

# The splits to load

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
#sample_id = dataset.view().first().id
view = dataset.view()

# Step 3: Send samples to Label Studio

# A unique identifier for this run
anno_key = "fiftyone_tredfddesddr3fdt3d323e"

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
    api_key="94b10acd4d3af0f7026cde0ab8a8fb8a60a3a6ef",
    launch_editor=True,
    timeout=1000
)
print(dataset.get_annotation_info(anno_key), "fatemeh ")