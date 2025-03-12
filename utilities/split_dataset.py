import os
import shutil
import random

subset_dir = "deep_darts_d2_dataset"

all_images_dir = os.path.join(subset_dir, "images", "train")
json_labels_dir = os.path.join(subset_dir, "labels", "train")

train_image_dir = os.path.join(subset_dir, 'images', 'train')
val_image_dir = os.path.join(subset_dir, 'images', 'val')
train_json_dir = os.path.join(subset_dir, 'labels', 'train')
val_json_dir = os.path.join(subset_dir, 'labels', 'val')

for dir_path in [train_image_dir, val_image_dir, train_json_dir, val_json_dir]:
    os.makedirs(dir_path, exist_ok=True)

all_images = [file for file in os.listdir(all_images_dir) if file.endswith('.JPG')]

random.seed(44)
random.shuffle(all_images)

split_index = int(len(all_images) * 0.8)

train_images = all_images[:split_index]
val_images = all_images[split_index:]

def copy_files(file_list, src_img_dir, src_json_dir, dst_img_dir, dst_json_dir):
    for file in file_list:
        src_img_path = os.path.join(src_img_dir, file)
        src_json_path = os.path.join(src_json_dir, file.replace('.JPG', '.json'))

        dst_img_path = os.path.join(dst_img_dir, file)
        dst_json_path = os.path.join(dst_json_dir, os.path.basename(src_json_path))

        if os.path.exists(src_img_path):
            shutil.move(src_img_path, dst_img_path)

        if os.path.exists(src_json_path):
            shutil.move(src_json_path, dst_json_path)

copy_files(train_images, all_images_dir, json_labels_dir, train_image_dir, train_json_dir)
copy_files(val_images, all_images_dir, json_labels_dir, val_image_dir, val_json_dir)

print("Dataset split completed successully!")
