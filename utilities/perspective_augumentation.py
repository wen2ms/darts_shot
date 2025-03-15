import cv2
import json
import numpy as np
import os 
import random
from glob import glob

keypoints_class = ['top', 'bottom', 'left', 'right']

def extract_images_keypoints(image_path, json_path):
    image = cv2.imread(image_path)

    with open(json_path, 'r') as infile:
        data = json.load(infile)

    keypoints = []
    for shape in data['shapes']:
        if shape['label'] in keypoints_class:
            keypoints.append(shape['points'][0])
    
    keypoints = np.array(keypoints, dtype=np.float32)

    return image, keypoints, data

def apply_perspective_transform(image, keypoints, perspective_matrix):
    height, width = image.shape[:2]
    
    transformed_image = cv2.warpPerspective(image, perspective_matrix, (width, height))

    keypoints = np.array([keypoints], np.float32)
    transformed_keypoints = cv2.perspectiveTransform(keypoints, perspective_matrix)[0]

    return transformed_image, transformed_keypoints

def save_augmented_data(image, keypoints, orignal_json_data, output_image_path, output_json_path):
    cv2.imwrite(output_image_path, image)

    keypoint_index = 0
    for shape in orignal_json_data['shapes']:
        if shape['label'] in keypoints_class:
            shape['points'] = [keypoints[keypoint_index].tolist()]
            keypoint_index += 1

    output_json_dir = os.path.dirname(output_json_path)
    orignal_json_data['imagePath'] = os.path.relpath(output_image_path, start=output_json_dir)

    with open(output_json_path, 'w') as outfile:
        json.dump(orignal_json_data, outfile, indent=2)

def augument_dataset(input_iamge_dir, input_json_dir, output_image_dir, output_json_dir, perspective_matrix, num_agumentations=1):
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_json_dir, exist_ok=True)

    images_path = glob(os.path.join(input_iamge_dir, '*.JPG'))

    for image_path in images_path:
        filename = os.path.basename(image_path)
        json_path = os.path.join(input_json_dir, filename.replace('.JPG', '.json'))

        if not os.path.exists(json_path):
            continue

        for i in range(num_agumentations):
            image, keypoints, original_json_data = extract_images_keypoints(image_path, json_path)

            transformed_image, transformed_keypoints = apply_perspective_transform(image, keypoints, perspective_matrix)

            output_image_path = os.path.join(output_image_dir, f'{filename[:-4]}_aug{i}.JPG')
            output_json_path = os.path.join(output_json_dir, f'{filename[:-4]}_aug{i}.json')

            save_augmented_data(transformed_image, transformed_keypoints, original_json_data, output_image_path, output_json_path)

def get_perspective_matrix(source_image_path, reference_image_path):
    with open(source_image_path.replace('.png', '.json'), 'r') as infile:
        source_data = json.load(infile)

    source_keypoints = []
    for shape in source_data['shapes']:
        source_keypoints.append(shape['points'][0])

    with open(reference_image_path.replace('.JPG', '.json'), 'r') as infile:
        destination_data = json.load(infile)

    destination_keypoints = []
    for shape in destination_data['shapes']:
        destination_keypoints.append(shape['points'][0])

    source_points = np.array(source_keypoints, dtype=np.float32)

    image = cv2.imread(source_image_path)

    destination_points = np.array(destination_keypoints,  dtype=np.float32)
    
    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)

    height, width = image.shape[:2]
    
    transformed_image = cv2.warpPerspective(image, perspective_matrix, (width, height))

    transformed_image_path = f'{source_image_path[:-4]}_transformed.png'
    cv2.imwrite(transformed_image_path, transformed_image)

    return perspective_matrix

input_image_dir = 'deep_darts_d2_dataset_augmented/images/train'
input_label_dir = 'deep_darts_d2_dataset_augmented/labels/train'

output_image_dir = 'deep_darts_d2_dataset_augmented/augmented_images/train'
output_label_dir = 'deep_darts_d2_dataset_augmented/augmented_labels/train'

perspective_image_path = 'perspective_images/scaled_image.png'
reference_image_path = 'perspective_images/reference.JPG'

perspective_matrix = get_perspective_matrix(perspective_image_path, reference_image_path)

perspective_matrix = np.linalg.inv(perspective_matrix)

augument_dataset(input_image_dir, input_label_dir, output_image_dir, output_label_dir, perspective_matrix)

print("Dataset augmented completed successully!")


