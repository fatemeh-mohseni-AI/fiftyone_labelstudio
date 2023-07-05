** my env: ubuntu 20.04 python 3.8.10 **

just install label-studio version 1.7.3 on 
version 1.8.0 faces an unrecognized weired error shown as below :

<< raise ValidationError(f'{ext} extension is not supported') >>

so install noted version . 
after first run django will return an error due to limitation on upload file numbers and is does not related to label-studio .
it is a Django limitation . i changed directly the line of code from the line :

<< venv/lib/python3.8/site-packages/django/http/multipartparser.py", line 242 >>
and change 
<< settings.DATA_UPLOAD_MAX_NUMBER_FILES >> to number 1000 . so it compare number of uploaded files with 1000 not the django setting .


run label-studio first , then run label_studio_upload.py .

NOTE :
the tree is as follows :

dir/
|
------dataset.yaml
------images
      |
       ---train
       ---test
------labels
      |
       ---train
       ---test

and dataset.yaml content looks like : 
-----------------------------------------------------
                                                    |
                                                    \/
train: ./images/traitrain: ./images/train/
val: ./images/val/

# number of classes
nc: 5

# class names
names: ["clean_water_pot", "dirty_water_pot", "feeding_line", "feeding_pot", "watering_line"]n/
val: ./images/val/

# number of classes
nc: 5

# class names
names: ["clean_water_pot", "dirty_water_pot", "feeding_line", "feeding_pot", "watering_line"]