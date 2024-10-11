from paddleocr import PaddleOCR

def extract_text_from_image(image_path):
    # Initialize the OCR model
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # You can specify 'ch' for Chinese or other supported languages
    
    # Perform OCR on the image
    result = ocr.ocr(image_path, cls=True)
    
    # Extracting the recognized text from the result
    extracted_text = []
    for line in result:
        for box in line:
            extracted_text.append(box[1][0])  # box[1][0] contains the recognized text
    
    # Return the concatenated text or as a list
    return " ".join(extracted_text)

# Example usage
image_path = r'/home/thahseer/Desktop/Nigeria_Data_Preperation/NIGERIA/Nigeria_2.png'
text = extract_text_from_image(image_path)
print("Extracted Text:", text)
