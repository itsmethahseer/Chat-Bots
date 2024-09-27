#!/usr/bin/env python3

import os
import cv2
import numpy as np

SRC_IMG_DIR = "/home/arjun123/PIXL/Augmentation/LabourCard/rotated_resized_imgs/"
DST_IMG_DIR = "/home/arjun123/PIXL/Augmentation/LabourCard/resized_images"
DST_MSK_DIR = "/home/arjun123/PIXL/Augmentation/LabourCard/resized_masks"

# create the destination folders if they do not exist, you can use the os.makedirs() function
if not os.path.exists(DST_IMG_DIR):
    os.makedirs(DST_IMG_DIR)

if not os.path.exists(DST_MSK_DIR):
    os.makedirs(DST_MSK_DIR)
    
def resize(image, width):
    """Resize image to be 'width' pixels wide maintaining the aspect ratio"""

    r = width / image.shape[1]
    dim = (width, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

if __name__ == '__main__':
    for i in os.listdir(SRC_IMG_DIR):
        image_path = os.path.join(SRC_IMG_DIR, i)
        print(image_path)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image {image_path}")
            continue
        image = resize(image, 640)
        cv2.imwrite(os.path.join(DST_IMG_DIR, i), image)

        mask = np.ones_like(image) * 255
        cv2.imwrite(os.path.join(DST_MSK_DIR, i), mask)
    
    for i in os.listdir(DST_IMG_DIR):
        image_path = os.path.join(DST_IMG_DIR, i)
        image = cv2.imread(image_path)
        print(image.shape)

    for i in os.listdir(DST_MSK_DIR):
        image_path = os.path.join(DST_MSK_DIR, i)
        image = cv2.imread(image_path)
        print(image.shape)