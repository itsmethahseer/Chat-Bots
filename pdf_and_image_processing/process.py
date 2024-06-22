import os
import cv2

def resize(image, width):
    """Resize image to be 'width' pixels wide maintaining the aspect ratio"""
    r = width / image.shape[1]
    dim = (width, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

def process_images_in_directory(directory_path, width):
    # Loop through all the files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Check if the file is an image (you can add more file extensions if needed)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            # Load the image
            image = cv2.imread(file_path)
            
            # Check if the image was loaded successfully
            if image is not None:
                # Resize the image
                resized_image = resize(image, width)
                
                # Save the resized image back to the same path
                cv2.imwrite(file_path, resized_image)
                print(f"Processed and saved: {file_path}")
            else:
                print(f"Failed to load image: {file_path}")

if __name__ == "__main__":
    # Directory containing the images
    directory_path = r'/home/thahseer/Downloads/output_credable/Qingdao'
    # Desired width to resize images to
    desired_width = 800  # Change this to the desired width
    
    # Process all images in the directory
    process_images_in_directory(directory_path, desired_width)
