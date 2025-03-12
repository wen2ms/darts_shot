import os
import shutil
import json

subset_dir = 'deep_darts_d2_dataset'

train_image_dir = os.path.join(subset_dir, 'images', 'train')
val_image_dir = os.path.join(subset_dir, 'images', 'val')
train_json_dir = os.path.join(subset_dir, 'labels', 'train')
val_json_dir = os.path.join(subset_dir, 'labels', 'val')

bbox_class = {'dartboard' : 0}
keypoints_class = ['top', 'bottom', 'left', 'right']

darts_shot_150_dataset = 'deep_darts_d2_dataset_final'

final_train_image_dir = os.path.join(darts_shot_150_dataset, 'images', 'train')
final_val_image_dir = os.path.join(darts_shot_150_dataset, 'images', 'val')
final_train_yolo_dir = os.path.join(darts_shot_150_dataset, 'labels', 'train')
final_val_yolo_dir = os.path.join(darts_shot_150_dataset, 'labels', 'val')

for dir_path in [final_train_image_dir, final_val_image_dir, final_train_yolo_dir, final_val_yolo_dir]:
    os.makedirs(dir_path, exist_ok=True)

def lableme2yolo(src_json_path, dst_yolo_path):
    with open(src_json_path, 'r') as infile:
        label_json = json.load(infile)

    img_width = label_json['imageWidth']
    img_height = label_json['imageHeight']

    yolo_label = ''
    all_keypoints = {}

    for shape in label_json['shapes']:
        if shape['shape_type'] == 'rectangle':
            bbox_class_id = bbox_class[shape['label']]

            x_min = min(shape['points'][0][0], shape['points'][1][0])
            x_max = max(shape['points'][0][0], shape['points'][1][0])
            y_min = min(shape['points'][0][1], shape['points'][1][1])
            y_max = max(shape['points'][0][1], shape['points'][1][1])

            x_center = (x_min + x_max) * 0.5
            y_center = (y_min + y_max) * 0.5

            bbox_width = x_max - x_min
            bbox_height = y_max - y_min

            norm_x_center = x_center / img_width
            norm_y_center = y_center / img_height

            noem_bbox_width = bbox_width / img_width
            noem_bbox_height = bbox_height / img_height

            yolo_label += f'{bbox_class_id} {norm_x_center:.6f} {norm_y_center:.6f} {noem_bbox_width:.6f} {noem_bbox_height:.6f} '
        elif shape['shape_type'] == 'point':
            norm_point_x = shape['points'][0][0] / img_width
            norm_point_y = shape['points'][0][1] /img_height

            point_label = shape['label']

            all_keypoints[point_label] = [norm_point_x, norm_point_y]

    for keypoint_class in keypoints_class:
        yolo_label += f'{all_keypoints[keypoint_class][0]:.6f} {all_keypoints[keypoint_class][1]:.6f} 2 '

    with open(dst_yolo_path, 'w') as outfile:
        outfile.write(yolo_label + '\n')

def copy_convert_files(file_list, src_img_dir, src_json_dir, dst_img_dir, dst_yolo_dir):
    for file in file_list:
        src_img_path = os.path.join(src_img_dir, file)
        src_json_path = os.path.join(src_json_dir, file.replace('.JPG', '.json'))

        dst_img_path = os.path.join(dst_img_dir, file)
        dst_yolo_path = os.path.join(dst_yolo_dir, file.replace('.JPG', '.txt'))

        lableme2yolo(src_json_path, dst_yolo_path)

        if os.path.exists(src_img_path):
            shutil.copy2(src_img_path, dst_img_path)

train_images = [file for file in os.listdir(train_image_dir) if file.endswith('.JPG')]
val_images = [file for file in os.listdir(val_image_dir) if file.endswith('.JPG')]

copy_convert_files(train_images, train_image_dir, train_json_dir, final_train_image_dir, final_train_yolo_dir)
copy_convert_files(val_images, val_image_dir, val_json_dir, final_val_image_dir, final_val_yolo_dir)

print("Dataset convert completed successully!")


        




