import os
from pdf2image import convert_from_path

# Path to the folder containing PDF files
pdf_folder_path = r'/home/thahseer/Downloads/CREDABLE_VENDOR_WISE_ INVOICES/Qingdao'

# Path to the output folder for JPEG images
output_folder_path = r'/home/thahseer/Downloads/output_credable/Qingdao'

# Ensure the output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# List all PDF files in the folder
pdf_files = [f for f in os.listdir(pdf_folder_path) if f.lower().endswith('.pdf')]

# Process each PDF file
for pdf_file in pdf_files:
    # Path to the current PDF file
    pdf_path = os.path.join(pdf_folder_path, pdf_file)
    
    # Convert PDF to images
    pages = convert_from_path(pdf_path, dpi=300)
    
    # Get the base name of the PDF file without extension
    base_name = os.path.splitext(pdf_file)[0]
    
    # Save each page as a JPEG image
    for i, page in enumerate(pages):
        # Define the output path for each image
        image_path = os.path.join(output_folder_path, f'{base_name}_{i + 1}.jpg')
        # Save the image
        page.save(image_path, 'JPEG')
    
    print(f'Converted {pdf_file} to images.')

print('All PDF files have been successfully converted to JPEG images.')