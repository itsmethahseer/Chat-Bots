from PIL import Image
import torch
import requests
from transformers import AutoProcessor, LlavaForConditionalGeneration

class ImageAssistant:
    def __init__(self, model_name="llava-hf/llava-1.5-7b-hf"):
        self.model = LlavaForConditionalGeneration.from_pretrained(model_name)
        self.processor = AutoProcessor.from_pretrained(model_name)
    
    def process_image_and_generate_response(self, url, prompt="USER: <image>\n Give me step by step process in the provided workflow image ASSISTANT:"):
        image = self._load_image(url)
        inputs = self.processor(text=prompt, images=image, return_tensors="pt")
        generate_ids = self.model.generate(**inputs, max_new_tokens=1000)
        response = self.processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return response
    
    def _load_image(self, url):
        image = Image.open(requests.get(url, stream=True).raw)
        return image
