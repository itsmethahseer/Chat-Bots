""" code for testing Gliner NER model for predicting the entities"""
import spacy
from spacy.language import Language
from spacy.tokens import Span
import re
import warnings
import time
from paddleocr import PaddleOCR, draw_ocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import interpolation as inter
from PIL import Image

# Mock imports, replace with actual library imports
import gliner_spacy
from gliner_spacy.pipeline import GlinerSpacy
from gliner import GLiNER

warnings.filterwarnings("ignore", message="The sentencepiece tokenizer that you are converting to a fast tokenizer uses the byte fallback option which is not implemented in the fast tokenizers.")
warnings.filterwarnings("ignore", message="resume_download is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use force_download=True.")

# Configuration for GLiNER integration
custom_spacy_config = {
    "gliner_model": "urchade/gliner_medium-v2.1",
    "chunk_size": 250,
    "labels": ["SURNAME", "FIRST NAME", "MIDDLE NAME", "DATE OF BIRTH", "ISSUE DATE", "NATIONALITY", "SEX","HEIGHT","DOCUMENTNO","EXPIRY","SERIAL"],
    "style": "ent",
    "threshold": 0.4
}

# Initialize a blank English spaCy pipeline and add GLiNER
nlp = spacy.blank("en")
nlp.add_pipe("gliner_spacy", config=custom_spacy_config)

# Initialize GLiNER model
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

class OCRCLASS:
    ocr = None
    
    @classmethod
    def load(cls):
        cls.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='en',
            debug=False,
            show_log=False,
            use_gpu=False,
            rec_batch_num=1,
            cls_batch_num=1,
            enable_mkldnn=True,
            cpu_threads=2
        )

# Function to extract text from image using PaddleOCR
def extract_text_from_image(image):
    result = OCRCLASS.ocr.ocr(image, cls=True)

    extracted_text = ""
    for line in result:
        for text_line in line:
            extracted_text += text_line[1][0] + " "
    return extracted_text.strip()

# Function to process text and extract named entities
def extract_entities(text):
    start_time = time.time()
    doc = nlp(text)

    # Consolidate consecutive address tokens into a single entity
    consolidated_entities = []
    current_address = []

    for ent in doc.ents:
        if ent.label_ == "ADDRESS":
            current_address.append(ent.text)
        else:
            if current_address:
                consolidated_entities.append({"text": ", ".join(current_address), "label": "ADDRESS"})
                current_address = []
            consolidated_entities.append({"text": ent.text, "label": ent.label_})

    if current_address:
        consolidated_entities.append({"text": ", ".join(current_address), "label": "ADDRESS"})

    inference_time = time.time() - start_time
    return consolidated_entities, inference_time

DEBUG = True

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

# Load OCR model
OCRCLASS.load()

# Example image path
img_path = r"/home/thahseer/Downloads/NIGERIA-20240704T100209Z-001 (1)/NIGERIA/Screenshot 2024-06-21 103755.png"
print(img_path)  
img = cv2.imread(img_path, cv2.IMREAD_COLOR)

skew = correct_skew(img)
gray_skew = cv2.cvtColor(skew, cv2.COLOR_BGR2GRAY)

extracted_text = extract_text_from_image(skew)
print("Extracted Text:\n", extracted_text)

# Pattern to match dates with spaces (e.g., "09 NOV 2016")
date_pattern = re.compile(r'(\d{2})\s*([A-Z]{3})\s*(\d{2})')

# Function to remove spaces in the matched dates
def remove_spaces_in_dates(match):
    return f"{match.group(1)}{match.group(2)}{match.group(3)}"

# Replace dates with spaces using the function
text1 = date_pattern.sub(remove_spaces_in_dates, extracted_text)

print("Updated Text:")
print(text1)

plt.imshow(skew)

# Extract entities from the text
entities, inference_time = extract_entities(text1)
print("\nExtracted Entities:")
for entity in entities:
    print(f"{entity['label']} => {entity['text']}")

print("Inference time:", inference_time, "seconds")
