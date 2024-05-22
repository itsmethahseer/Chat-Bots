import os
import re
from functions import Gpt4Vision

azure_openai_api_key = os.getenv('AZURE_OPENAI_API_KEY')
config_file_path = "gpt4vision.yaml"  # Path to your config file
input_image_url = r"replace the input image url here." 

input_prompt = "your prompt here for image"
input_prompt_template = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": input_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "" ,
                                "detail": "low",
                            }
                        }
                    ]}
                ]




# Initialize Gpt4Vision
gpt_vision = Gpt4Vision(config_file_path)
# Get response
response = gpt_vision.get_response(input_image_url, input_prompt_template)
print(response)
print(input_image_url)