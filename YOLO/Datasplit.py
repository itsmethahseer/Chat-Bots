import os
import random
import shutil

def split_dataset(input_folder, output_folder, split_ratio=0.8):
    # Create the train and val directories
    train_images = os.path.join(output_folder, 'images/train')
    val_images = os.path.join(output_folder, 'images/val')
    train_labels = os.path.join(output_folder, 'labels/train')
    val_labels = os.path.join(output_folder, 'labels/val')

    os.makedirs(train_images, exist_ok=True)
    os.makedirs(val_images, exist_ok=True)
    os.makedirs(train_labels, exist_ok=True)
    os.makedirs(val_labels, exist_ok=True)

    # Get all image files (assuming annotations have the same name with .txt extension)
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]
    random.shuffle(image_files)

    split_idx = int(len(image_files) * split_ratio)
    train_files = image_files[:split_idx]
    val_files = image_files[split_idx:]

    # Function to move images and labels
    def move_files(file_list, src_folder, dst_image_folder, dst_label_folder):
        for image_file in file_list:
            label_file = image_file.rsplit('.', 1)[0] + '.txt'  # Assuming YOLO annotation files are .txt

            # Move the image
            shutil.copy(os.path.join(src_folder, image_file), os.path.join(dst_image_folder, image_file))

            # Move the corresponding annotation if it exists
            if os.path.exists(os.path.join(src_folder, label_file)):
                shutil.copy(os.path.join(src_folder, label_file), os.path.join(dst_label_folder, label_file))

    # Move training files
    move_files(train_files, input_folder, train_images, train_labels)

    # Move validation files
    move_files(val_files, input_folder, val_images, val_labels)

    print(f"Dataset split complete! {len(train_files)} for training and {len(val_files)} for validation.")

# Example usage:
input_folder = r'/home/thahseer/Desktop/Nigeria_Data_Preperation/final_set/images'  # Folder containing both images and annotations
output_folder = './DataTrain'
split_dataset(input_folder, output_folder, split_ratio=0.8)
