from functions import (
    load_embedding_model,
    create_embeddings,
    load_qa_chain,
    get_response,
    split_documents,
    pdf_loader,
    template,
)
from ctransformers import AutoModelForCausalLM

from langchain.prompts import PromptTemplate



# Loading orca-mini from Ollama
llm = AutoModelForCausalLM.from_pretrained("TheBloke/Ferret_7B-GGUF", model_file="ferret_7b.Q4_K_M.gguf", model_type="mistral", gpu_layers=50)

# Loading the Embedding Model
embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

# loading and splitting the documents
docs = pdf_loader(
    file_path="/home/c847/Desktop/whizz/Ferrot/data/alzheimers-dementia-about-alzheimers-disease-ts.pdf"
)
documents = split_documents(documents=docs)

# creating vectorstore
vectorstore = create_embeddings(documents, embed)

# converting vectorstore to a retriever
retriever = vectorstore.as_retriever()

# Creating the prompt from the template which we created before
prompt = PromptTemplate.from_template(template)

# Creating the chain
chain = load_qa_chain(retriever, llm, prompt)


question = "What is Alzheimer's disease?"
response = get_response(question, chain)
print("Response:", response)