import os
import pandas as pd
import json

dataset_dir = 'deep_darts_dataset'
images_dir = os.path.join(dataset_dir, 'images')

file_path = os.path.join(dataset_dir, 'labels.pkl')
dataframe = pd.read_pickle(file_path)

output_dir = os.path.join(dataset_dir, 'labels')
os.makedirs(output_dir, exist_ok=True)

img_width, img_height = 800, 800

keypoints_label = ['top', 'bottom', 'left', 'right']

for index, row in dataframe.iterrows():
    dir_name = row.iloc[0]
    img_name = row.iloc[1]

    keypoints = row.iloc[3][:4]

    absolute_keypoints = [[keypoint[0] * img_width, keypoint[1] * img_height] for keypoint in keypoints]

    dir_path = os.path.join(output_dir, dir_name)
    os.makedirs(dir_path, exist_ok=True)

    image_path = os.path.join(images_dir, dir_name, img_name)

    json_data = {
        "version": "5.6.0",
        "flags": {},
        "shapes": 
        [
            {
                "label": "dartboard",
                "points": [[0.0, 0.0], [img_width, img_height]],
                "group_id": None,
                "description": "",
                "shape_type": "rectangle",
                "flags": {},
                "mask": None
            }
        ] + 
        [
            {
                "label": keypoints_label[i], 
                "points": [absolute_keypoints[i]],
                "group_id": None,
                "description": "",
                "shape_type": "point",
                "flags": {},
                "mask": None
            } for i in range(4)
        ], 
        "imagePath": os.path.relpath(image_path, start=dir_path),
        "imageData": None,
        "imageHeight": img_height,
        "imageWidth": img_width
    }

    label_file_name = img_name.replace('.JPG', '.json')
    label_file_path = os.path.join(dir_path, label_file_name)

    with open(label_file_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=2)

print("Labelme labels extracted successfully!")


