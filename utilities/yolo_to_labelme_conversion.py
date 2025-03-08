import os 
import json

def convert_yolo_to_labelme(yolo_txt_path, labelme_json_path, image_path):
    json_data = {
        "version": "5.6.0",
        "flags": {},
        "shapes": [], 
        "imagePath": os.path.relpath(image_path, start=labelme_labels_dir),
        "imageData": None,
        "imageHeight": 1080,
        "imageWidth": 1920
    }

    with open(yolo_txt_path, 'r') as infile:
        lines = infile.readlines()

        for line in lines:
            parts = line.strip().split()

            x_center, y_center, width, height = map(float, parts[1:])

            x_min = (x_center - width / 2) * json_data["imageWidth"]
            y_min = (y_center - height / 2) * json_data["imageHeight"]
            x_max = (x_center + width / 2) * json_data["imageWidth"]
            y_max = (y_center + height / 2) * json_data["imageHeight"]

            shape = {
                "label": "dartboard",
                "points": [[x_min, y_min], [x_max, y_max]],
                "group_id": None,
                "description": "",
                "shape_type": "rectangle",
                "flags": {},
                "mask": None
            }

            json_data["shapes"].append(shape)

    with open(labelme_json_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=2)

subset_dir = "darts_shot_sub_dataset"
subset_images_dir = os.path.join(subset_dir, "images", "train", "b1_03_05_2025")

yolo_labels_dir = os.path.join(subset_dir, "labels", "train", "b1_03_05_2025")
labelme_labels_dir = os.path.join(subset_dir, "json_labels", "train", "b1_03_05_2025")

os.makedirs(labelme_labels_dir, exist_ok=True)

all_yolo_files = [file for file in os.listdir(yolo_labels_dir) if file.endswith('.txt')]

for yolo_file in all_yolo_files:
    yolo_txt_path = os.path.join(yolo_labels_dir, yolo_file)
    labelme_json_path = os.path.join(labelme_labels_dir, yolo_file.replace('.txt', '.json'))

    image_path = os.path.join(subset_images_dir, yolo_file.replace('.txt', '.png'))

    convert_yolo_to_labelme(yolo_txt_path, labelme_json_path, image_path)

print("Conversion completed successfully!")


