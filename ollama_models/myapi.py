from fastapi import FastAPI, Form
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import asyncio
import textwrap
from main import (
    load_embedding_model,
    create_embeddings,
    load_qa_chain,
    get_response,
    split_documents,
    pdf_loader,
    template,
)
from langchain.llms.ollama import Ollama
from langchain.prompts import PromptTemplate

app = FastAPI()

# Paste your main code here (import statements, functions, etc.)

# Loading orca-mini from Ollama
llm = Ollama(model="orca-mini", temperature=0)

# Loading the Embedding Model
embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

# loading and splitting the documents
docs = pdf_loader(
    file_path="/home/c847/Desktop/Chatbots with LLms/ollama_models/data/instapdf.in-independence-day-speech-english-423.pdf"
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


async def get_response_incremental(question, chain):
    # Getting response from chain
    response = chain({"query": question})

    # Split the response into chunks
    chunks = response["result"].split("\n")

    # Use an asynchronous generator to yield chunks
    for chunk in chunks:
        # Wrap the text for better output
        wrapped_chunk = textwrap.fill(chunk, width=100)
        yield wrapped_chunk
        await asyncio.sleep(0.5)

@app.post("/chatbot")
async def chatbot_endpoint(question: str = Form(...)):
    # Getting response from the chatbot
    response_generator = get_response_incremental(question, chain)

    # Collecting all chunks of the response
    response_chunks = [chunk async for chunk in response_generator]

    # Joining the response chunks into a single string
    full_response = "\n".join(response_chunks)
    cleaned_response = full_response.replace("\n", " ")

    # Returning the response
    return {"response": cleaned_response}
