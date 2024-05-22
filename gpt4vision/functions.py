from langchain_openai import AzureChatOpenAI
from openai import BadRequestError
import copy
import asyncio
import base64
import yaml
import os




def image_to_base64(image_path):
    if image_path.endswith(('.jpg', '.jpeg', '.png')):
        with open(image_path, "rb") as image_file: #'rb' read binary
            encoded = base64.b64encode(image_file.read())
            decode = encoded.decode('utf-8')

            #Add text for data URI format
            encoded_string = f'data:image/jpeg;base64,{decode}'
    else:
        raise Exception("Invalid Input Format")

   
    return encoded_string



def update_base64_image(base64_image, input_prompt_template):

    # Create a deep copy of the input prompt template to ensure each iteration operates on a unique instance 
    updated_prompt = copy.deepcopy(input_prompt_template)
    # Iterate over the list
    for item in updated_prompt:
        # Check if the item is a dictionary and contains the key "content"
        if isinstance(item, dict) and "content" in item:
            content = item["content"]
            # Check if the content is a list and contains dictionaries
            if isinstance(content, list):
                for sub_item in content:
                    # Check if the sub_item is a dictionary and contains the key "image_url"
                    if isinstance(sub_item, dict) and "image_url" in sub_item:
                        image_url = sub_item["image_url"]
                        # Check if the image_url is a dictionary and contains the key "url"
                        if isinstance(image_url, dict) and "url" in image_url:
                            # Update the value of "url"
                            image_url["url"] = base64_image
    return updated_prompt



class Gpt4Vision:

    #Load vision model configuration files
    def __init__(self, config_path):
        try:
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Config file '{config_path}' not found.")
            

            with open(config_path, 'r') as yaml_file:
                self.configs = yaml.safe_load(yaml_file) #add error handling to check config file is valid, path correct, file present
            

            # Check if necessary configurations are present in loaded config file
            required_configs = ['GPT4_VISION_DEPLOYMENT_NAME', 'GPT4_VISION_API_VERSION', 'GPT4_VISION_MAX_TOKENS']
            for config in required_configs:
                if config not in self.configs:
                    raise ValueError(f"Configuration '{config}' not found in the config file.")
                
            self.deployment_name = self.configs['GPT4_VISION_DEPLOYMENT_NAME']
            self.max_tokens = self.configs['GPT4_VISION_MAX_TOKENS']
            api_version = self.configs['GPT4_VISION_API_VERSION']
            api_key = self.configs['GPT4_VISION_KEY']
            
            
            # Initialization of GPT4 Vision using Langchain
            self.gpt4v_client = AzureChatOpenAI(
                azure_deployment = self.deployment_name,
                api_version=api_version,  max_tokens = self.max_tokens, api_key=api_key, temperature=0.0, streaming=True
            )
        except FileNotFoundError as e:
            raise Exception("Error Loading Config File")
        except Exception as e:
            # Handle ValidationError here
            raise Exception("Validation Error from AzureChatOpenAI")

    def get_response(self, input_path, input_prompt):

            
            
            base64_image = image_to_base64(input_path)
            # Update input prompt with base64 image
            input_prompt = update_base64_image(base64_image,input_prompt)
            model_response = self.gpt4v_client.invoke(
                        input = input_prompt
                    )
            
            return model_response
    