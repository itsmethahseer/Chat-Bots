# Mamba is a newly released Large language model\
# interesting thing is that it is not transformer based model , it is RNN based.


import torch
from transformers import AutoTokenizer
from mamba_ssm.models.mixer_seq_simple import MambaLMHeadModel

device = "cpu"
tokenizer = AutoTokenizer.from_pretrained("havenhq/mamba-chat")
tokenizer.eos_token = "<|endoftext|>"
tokenizer.pad_token = tokenizer.eos_token
tokenizer.chat_template = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-beta").chat_template

model = MambaLMHeadModel.from_pretrained("havenhq/mamba-chat", device="cuda", dtype=torch.float16)