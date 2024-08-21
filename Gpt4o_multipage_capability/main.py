"""Using this code we can process multiple images in a pdf as base64 and pass it into Gpt4-o to get response in a structured format"""

import os
import openai
from pdf2image import convert_from_path
import base64

openai.api_key = "your key here"

def pdf_to_image_list(pdf_path):
    images = convert_from_path(pdf_path)
    return images

pdf_path = "/home/thahseer/Downloads/samples1/ilovepdf_merged.pdf"

# Convert PDF to list of images
images = pdf_to_image_list(pdf_path)
print(images)

# Prepare the images for the API call
image_messages = []
for image in images:
    image.save("temp_image.jpeg")
    with open('temp_image.jpeg', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    image_messages.append(
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            }
        }
    )

# Add text content to the messages
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Extract the Main details from the document in JSON structure"},
        ] + image_messages
    }
]

# Send request to OpenAI API
response = openai.chat.completions.create(
    model='gpt-4o',
    messages=messages,
    max_tokens=4000,
)

# Print or process the response
print(response.choices[0].message.content)
print("type:", type(response.choices[0].message.content))