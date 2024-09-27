#!/usr/bin/env python3

import glob
import os

import cv2

# Set your destination folder path
IMG_DIR = "/home/arjun123/PIXL/Augmentation/LabourCard/rotated_resized_imgs"
# Set your image width required
IMG_WIDTH = 1200

# Copy all your cropped and correctly oriented images to a folder named raw_cropped_images


def resizeH(image, width):
    """Resize image to be 'width' pixels wide maintaining the aspect ratio"""

    # calculates the scaling factor r 
    r = width / image.shape[1]
    dim = (width, int(image.shape[0] * r))
    # new height is calculated 
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    # "nterpolation=cv2.INTER_AREA", to reduce the aliasing effect when resizing images
    return resized


def resizeW(image, height):
    """Resize image to be 'width' pixels wide maintaining the aspect ratio"""

    r = height / image.shape[0]
    dim = (int(image.shape[1] * r), height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def resize_to_standard_size(image, size):
    h, w, _ = image.shape
    if w <= h:
        resized_image = resizeH(image, width=size)
    else:
        resized_image = resizeW(image, height=size)
    return resized_image


def resize():
    i = 1
    for file in glob.glob("/home/arjun123/PIXL/Augmentation/LabourCard/data/*"):
        try:
            img_name = "resized_" + str(i) + ".jpg"
            image = cv2.imread(file)
            image = resize_to_standard_size(image, IMG_WIDTH)
            cv2.imwrite(os.path.join(IMG_DIR, img_name), image)
            i = i + 1
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")

def rotate():
    i = 1
    for file in glob.glob("/home/arjun123/PIXL/Augmentation/LabourCard/data/*"):
        try:
            image = cv2.imread(file)
            resized_image = resize_to_standard_size(image, IMG_WIDTH)

            # Save the correctly oriented (resized) image
            orig_img_name = "resized_" + str(i) + ".jpg"
            cv2.imwrite(os.path.join(IMG_DIR, orig_img_name), resized_image)

            # Save rotated versions
            rotations = {
                "rotated90_": cv2.ROTATE_90_COUNTERCLOCKWISE,
                "rotated90_clock_": cv2.ROTATE_90_CLOCKWISE,
                "rotated180_": cv2.ROTATE_180
            }

            for prefix, rotation in rotations.items():
                rotated_image = cv2.rotate(resized_image, rotation)
                img_name = prefix + str(i) + ".jpg"
                cv2.imwrite(os.path.join(IMG_DIR, img_name), rotated_image)

            i += 1
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")


def augment():
    # resize()
    rotate()


if __name__ == "__main__":
    augment()