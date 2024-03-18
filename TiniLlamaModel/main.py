from llama_index import SimpleDirectoryReader, ServiceContext
from llama_index.llms import HuggingFaceLLM
from langchain.document_loaders import UnstructuredPDFLoader
import torch

documents = UnstructuredPDFLoader("/home/c847/Desktop/Chatbots with LLms/TiniLlamaModel/data/instapdf.in-independence-day-speech-english-423.pdf").load_data()

print("Hello world")