import os
import cv2
import numpy as np
from scipy.ndimage import interpolation as inter
from scipy.ndimage import rotate

DEBUG = False  # Set to True if you want to see debug prints

def correct_skew(image, delta=1, limit=10):
    """Correcting the skewness in the image"""

    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    if DEBUG:
        print("Angle by which image is rotated: {}".format(best_angle))

    rotated_image = inter.rotate(image, best_angle, reshape=False, order=0)

    return rotated_image

def process_images_in_directory(directory_path):
    # Loop through all the files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Check if the file is an image (you can add more file extensions if needed)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            # Load the image
            image = cv2.imread(file_path)
            
            # Correct skew
            corrected_image = correct_skew(image)
            
            # Save the corrected image back to the same path
            cv2.imwrite(file_path, corrected_image)
            print(f"Processed and saved: {file_path}")

if __name__ == "__main__":
    # Directory containing the images
    directory_path = r'/home/thahseer/Downloads/output_credable/Qingdao'
    
    # Process all images in the directory
    process_images_in_directory(directory_path)
