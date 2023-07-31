import os

dir = "/mnt/extra/Datasets/v2_p/no_dead_sick**/bad_size"
files = os.listdir(dir)
os.chdir(dir)
for i in range(1, len(files)):
  os.rename(files[i], f'chickenp_sdh_{i}.jpg')