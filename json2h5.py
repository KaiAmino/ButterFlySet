import os
import re
import cv2
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from PIL import Image
import random
import shutil
import argparse
import tqdm
import glob

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-json', '--json_directory', type = str, default = 'jsons')
parser.add_argument('-name', '--dataset_name', type = str, default = 'data_train')
parser.add_argument('-user', '--user', type = str, default = 'TY')
parser.add_argument('-mkvideo', '--make_video', type=lambda x: x.lower() in ('true', '1'), default = True)
parser.add_argument('-fps', '--video_fps', type = int, default = 60)
opt = parser.parse_args()

def split_list_into_groups(lst, group_size):
    return [lst[i:i + group_size] for i in range(0, len(lst), group_size)]

json_dir = opt.json_directory
name = opt.dataset_name
phase = name
user = opt.user

os.makedirs(os.path.join(name, 'dataset'), exist_ok = True)
os.makedirs(os.path.join(name, 'videos'), exist_ok = True)

# Making dataset files
print('Creating a dataset.')

json_dirs = sorted([item for item in os.listdir(json_dir) if item.startswith("OK_")], key=lambda x: int(x.split('_')[1]))

h5_output_path = os.path.join(name, 'dataset', 'CollectedData_' + user + '.h5')
csv_output_path = os.path.join(name, 'dataset', 'CollectedData_' + user + '.csv')
img_path_new = os.path.join(name, 'dataset')

h5_data = []
names = []
c = 1
for i in tqdm.tqdm(range(len(json_dirs))):
    jsons = os.listdir(os.path.join(json_dir, json_dirs[i]))
    jsons = sorted(jsons, key=lambda x: int(x.split('_')[2].split('.')[0]))

    for j in range(len(jsons)):
        f = open(os.path.join(json_dir, json_dirs[i], jsons[j]), 'r')
        d = json.load(f)

        img_name_original = d['name']
        img_name_new = 'img' + str(c).zfill(4) + '.jpg'
        shutil.copy2(os.path.join('original', d['name']), os.path.join(img_path_new, img_name_new))

        img_data = []

        for p in d['annotations'][0]['keypoints']:
            keypoint = p['key']
            coord_x = p['value'][0]
            coord_y = p['value'][1]
            img_data.append(coord_x)
            img_data.append(coord_y)

        h5_data.append(img_data)
        names.append(img_name_new)
        c = c + 1

scorers = [user] * 18
body_parts = ['head', 'thorax', 'abdomen', 
            'left_wing_1', 'left_wing_2', 'left_wing_3', 
            'right_wing_1', 'right_wing_2', 'right_wing_3']
bodyparts = [part for part in body_parts for _ in range(2)]
coords = ['x', 'y'] * 9

header = pd.MultiIndex.from_arrays([scorers, bodyparts, coords], names=['scorers', 'bodyparts', 'coords'])

index_col_1 = ['labeled-data'] * len(h5_data)
index_col_2 = [phase] * len(h5_data)
index_col_3 = names

multi_index = pd.MultiIndex.from_arrays([index_col_1, index_col_2, index_col_3])

df = pd.DataFrame(h5_data, columns=header, index=multi_index)
df = df.replace(0, np.nan)

with pd.HDFStore(h5_output_path, mode='w') as store:
    store.put('df_with_missing', df, format='fixed')
with open(csv_output_path, 'w') as f:
    df.to_csv(f)


# Making videos
if opt.make_video:
    print('Creating a video.')
    image_folder = os.path.join(name, 'dataset')
    output_video = os.path.join(name, 'videos', name + '.mp4')

    images = sorted(glob.glob(os.path.join(image_folder, "img*.jpg")))
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape
    fps = opt.video_fps
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    for i in tqdm.tqdm(range(len(images))):
        img_path = images[i]
        frame = cv2.imread(img_path)
        video.write(frame)
    video.release()
    cv2.destroyAllWindows()
