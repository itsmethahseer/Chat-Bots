import os

def remove_files_from_subdirectories(main_directory):
    # Walk through the main directory
    for root, dirs, files in os.walk(main_directory):
        for file in files:
            # Get the full path to the file
            file_path = os.path.join(root, file)
            try:
                # Remove the file
                os.remove(file_path)
                print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

if __name__ == "__main__":
    # Specify the main directory here
    main_directory = r'/home/thahseer/Downloads/output_credable'
    remove_files_from_subdirectories(main_directory)
    print("all files removed")