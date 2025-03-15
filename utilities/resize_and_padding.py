import cv2
import numpy as np

def resizing_with_padding(image_path, output_path, target_size=(800, 800)):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    if width > height:
        padding = (width - height) // 2
        padded_image = cv2.copyMakeBorder(image, padding, padding, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    else:
        padding = (height - width) // 2
        padded_image = cv2.copyMakeBorder(image, 0, 0, padding, padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    resized_image= cv2.resize(padded_image, target_size, interpolation=cv2.INTER_AREA)

    cv2.imwrite(output_path, resized_image)

if __name__ == "__main__":
    resizing_with_padding('perspective_images/image.png', 'perspective_images/scaled_image.png')