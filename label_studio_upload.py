import fiftyone as fo
import shutil
import os 
import glob
import time


dataset_dir = "/mnt/extra/Datasets/v4_aggregated/aggregated_checked_line_chicken"

def upload():
  # Step 1: Load your data into FiftyOne
  # A name for the dataset

  name = "label-chicken-train"

  # The directory containing the dataset to import
  dataset_type = fo.types.YOLOv5Dataset  # for example

  dataset = fo.Dataset.from_dir(
      dataset_dir=dataset_dir,
      dataset_type=dataset_type,
      )

  dataset.persistent = True
  view = dataset.view()

  # A unique identifier for this run
  anno_key = "change_this_line_12345"


  #dataset.distinct("line.instances.label"),

  label_schema = {
      "chicken": {
          "type": "detections", #  ['classification', 'detection', 'detections', 'instance', 'instances', 'polyline', 'polylines', 'polygon', 'polygons', 'keypoint', 'keypoints', 'segmentation', 'scalar']
          # "classes":['dead_chicken', 'healthy_chicken', 'sick_chicken']
          "classes":["clean_water_pot", "dirty_water_pot", "feeding_line", "feeding_pot", "watering_line", "dead", "healthy", "sick"],

      }
  }
  view.annotate(
      anno_key,
      project_name=name,
      backend="labelstudio",
      #label_schema=label_schema,
      label_field="ground_truth",
    #  url="http://localhost:8080",
      url="http://192.168.2.193",
    #  api_key="94b10acd4d3af0f7026cde0ab8a8fb8a60a3a6ef",  # check READ.ME file   local
      api_key="02e02bdf304115753da546aeb885ed47728a1e21",   # server
      #launch_editor=True,
  )


  print(dataset.get_annotation_info(anno_key))
  time.sleep(.3)

def spliter():
  x = input("input folders should called as labels_ and images_ ok ??")
  if not x == "y":
    raise NameError("enter y to agree")

  

  # Get the folder path
  folder_path = dataset_dir

  # Check if images and labels folders exist
  _images = os.path.join(folder_path, "images")   # to this
  _labels = os.path.join(folder_path, "labels")

  images_ = os.path.join(folder_path, "images_")   #from this
  labels_ = os.path.join(folder_path, "labels_")
  
  if os.path.exists(_images):
    if len(os.listdir(_images)) > 1:
      raise RuntimeError(" folder images should be renamed to images_ ")

  if not os.path.exists(images_) or not os.path.exists(labels_):
      print("images or labels folder does not exist!")
      exit()

  # Get list of image files       
  image_files = os.listdir(images_)
  # Create output folders       
  count = 0
  # Process files in batches of 150      
  for i in range(0, len(image_files), 150):
           
      os.makedirs(_images, exist_ok=True)
      os.makedirs(_labels, exist_ok=True)

      # Get image files for this batch   
      start = i     
      end = i + 150      
      batch_image_files = image_files[start:end]
      print(start, end, "start and end ")
      time.sleep(3)

      # Copy corresponding label files      
      for file in batch_image_files:
          # Copy image file
          file_path = os.path.join(images_, file)
          shutil.copy(file_path, _images)

          # Copy label file 
          try:
            _, ext = os.path.splitext(file_path)
            shutil.copy(os.path.join(labels_, file.replace(ext,".txt")), _labels)
          except:
            count+=1
            print("image has no label", count)


      # Do something with these 150 files here       
      upload()  
      files__ = glob.glob(_images+'/*')
      for f in files__:
        os.remove(f)

      files__ = glob.glob(_labels+'/*')
      for f in files__:
        os.remove(f)
      
def test():
  images_ = os.path.join(dataset_dir, "images")   #from this
  labels_ = os.path.join(dataset_dir, "labels")

  count_ = 0

  image_files = os.listdir(images_)
  labels_files = os.listdir(labels_)
  for i in image_files:
    file =os.path.join(images_, i)
    _, ext = os.path.splitext(file)
    j = i.replace(ext, ".txt")

    if j in labels_files:
      count_+=1
  print(count_)


spliter()