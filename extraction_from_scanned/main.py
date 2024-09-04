from pdf2image import convert_from_path
from PIL import Image
import pytesseract

def extract_text_from_scanned_pdf(pdf_path, output_text_file):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    all_text = ""

    # Iterate through all the images (pages)
    for image in images:
        # Use pytesseract to do OCR on the image
        ocr_text = pytesseract.image_to_string(image)
        all_text += ocr_text + "\n"

    # Write the extracted text to a text file
    with open(output_text_file, 'w', encoding='utf-8') as f:
        f.write(all_text)

# Example usage
pdf_path = "/home/thahseer/Downloads/repixlocrarconcontainer/Empty Yard/Madras container MCT408.pdf"
output_text_file = "output_text_file.txt"
extract_text_from_scanned_pdf(pdf_path, output_text_file)
