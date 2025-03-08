import os
import shutil

base_dir = "darts_shot_dataset"
images_dir = os.path.join(base_dir, "images", "train", "b1_03_05_2025")
labels_dir = os.path.join(base_dir, "labels", "train", "b1_03_05_2025")

subset_dir = "darts_shot_sub_dataset"
subset_images_dir = os.path.join(subset_dir, "images", "train", "b1_03_05_2025")
subset_labels_dir = os.path.join(subset_dir, "labels", "train", "b1_03_05_2025")

os.makedirs(subset_images_dir, exist_ok=True)
os.makedirs(subset_labels_dir, exist_ok=True)

all_images = [file for file in os.listdir(images_dir) if file.endswith('.png')]
all_images.sort(key=lambda image_file: os.path.getctime(os.path.join(images_dir, image_file)))

sub_images = all_images[:150]

for image_file in sub_images:
    image_path = os.path.join(images_dir, image_file)

    label_file = image_file.replace('.png', '.txt')
    label_path = os.path.join(labels_dir, label_file)

    shutil.copy(image_path, os.path.join(subset_images_dir, image_file))

    if os.path.exists(label_path):
        shutil.copy(label_path, os.path.join(subset_labels_dir, label_file))

print("First 150 images and corresponding labels copied successfully!")