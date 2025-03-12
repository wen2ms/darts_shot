import os
import shutil

source_dir = 'deep_darts_dataset'

image_source_dir = os.path.join(source_dir, 'images')
label_source_dir = os.path.join(source_dir, 'labels')

subset_output_dir = 'deep_darts_d2_dataset'
image_output_dir = os.path.join(subset_output_dir, 'images', 'train')
label_output_dir = os.path.join(subset_output_dir, 'labels', 'train')

os.makedirs(image_output_dir, exist_ok=True)
os.makedirs(label_output_dir, exist_ok=True)

def copy_files(source_dir, output_dir):
    for folder_name in os.listdir(source_dir):
        if folder_name.startswith('d2_'):
            folder_path = os.path.join(source_dir, folder_name)

            if os.path.isdir(folder_path):
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)

                    new_file_name = f'{folder_name}_{file_name}'

                    shutil.copy2(file_path, os.path.join(output_dir, new_file_name))

copy_files(image_source_dir, image_output_dir)
copy_files(label_source_dir, label_output_dir)

print('Images and labels have been successfully merged!')
