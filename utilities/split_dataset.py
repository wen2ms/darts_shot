import os
import shutil
import random
import argparse


class DatasetSplitter:
    def __init__(self, base_dir, image_ext='.png', label_ext='.txt', split_ratio=0.8, seed=44):
        self.base_dir = base_dir
        self.image_ext = image_ext
        self.label_ext = label_ext
        self.split_ratio = split_ratio
        self.seed = seed

        self.images_dir = os.path.join(base_dir, 'images', 'train')
        self.labels_dir = os.path.join(base_dir, 'labels', 'train')

        self.train_image_dir = os.path.join(base_dir, 'images', 'train')
        self.val_image_dir = os.path.join(base_dir, 'images', 'val')
        self.train_label_dir = os.path.join(base_dir, 'labels', 'train')
        self.val_label_dir = os.path.join(base_dir, 'labels', 'val')

        for d in [self.train_image_dir, self.val_image_dir, self.train_label_dir, self.val_label_dir]:
            os.makedirs(d, exist_ok=True)

    def split(self):
        all_images = [f for f in os.listdir(self.images_dir) if f.endswith(self.image_ext)]
        random.seed(self.seed)
        random.shuffle(all_images)

        split_idx = int(len(all_images) * self.split_ratio)
        train_images = all_images[:split_idx]
        val_images = all_images[split_idx:]

        self._move_files(train_images, self.train_image_dir, self.train_label_dir)
        self._move_files(val_images, self.val_image_dir, self.val_label_dir)

        print("✅ Dataset split completed successfully!")

    def _move_files(self, file_list, dst_img_dir, dst_label_dir):
        for file in file_list:
            src_img_path = os.path.join(self.images_dir, file)
            src_label_path = os.path.join(self.labels_dir, file.replace(self.image_ext, self.label_ext))

            dst_img_path = os.path.join(dst_img_dir, file)
            dst_label_path = os.path.join(dst_label_dir, os.path.basename(src_label_path))

            if os.path.exists(src_img_path):
                shutil.move(src_img_path, dst_img_path)
            if os.path.exists(src_label_path):
                shutil.move(src_label_path, dst_label_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_dir', required=True)
    parser.add_argument('--image_ext', default='.png')
    parser.add_argument('--label_ext', default='.txt')
    parser.add_argument('--split_ratio', type=float, default=0.8)
    parser.add_argument('--seed', type=int, default=44)
    return parser.parse_args()


def main():
    args = parse_args()
    splitter = DatasetSplitter(
        base_dir=args.dataset_dir,
        image_ext=args.image_ext,
        label_ext=args.label_ext,
        split_ratio=args.split_ratio,
        seed=args.seed
    )
    splitter.split()


if __name__ == '__main__':
    main()
