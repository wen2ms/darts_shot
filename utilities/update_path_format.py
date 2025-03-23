import os
import json


def update_image_path(filepath):
    with open(filepath, 'r') as infile:
        data = json.load(infile)

    data['imagePath'] = data['imagePath'].replace('\\', '/')

    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=2)


def update_all_json_files(directory):
    all_json_files = [file for file in os.listdir(directory) if file.endswith('.json')]

    for json_file in all_json_files:
        json_file_path = os.path.join(directory, json_file)

        update_image_path(json_file_path)


if __name__ == "__main__":
    subset_dir = 'darts_shot_sub_dataset'
    labels_dir = os.path.join(subset_dir, 'labels', 'train', 'b1_03_05_2025')

    update_all_json_files(labels_dir)

    print("Updating completed successfully!")