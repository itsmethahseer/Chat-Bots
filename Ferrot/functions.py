from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import textwrap
from ctransformers import AutoModelForCausalLM


def pdf_loader(file_path):
    loader = PyMuPDFLoader(file_path=file_path)
    # Loading the document file
    docs = loader.load()

    return docs


prompt = """
### System:
You are a helpful assistant. Synthesize an answer to the prompt by the user, \
in your words using the below input.If you cannot answer the question using \
the context, say 'I don't know the answer

### User:
{prompt}

### Response:

"""


template = """
### System:
You are an respectful and honest assistant. You have to answer the user's \
questions using only the context provided to you. If you don't know the answer, \
just say you don't know. Don't try to make up an answer.

### Context:
{context}

### User:
{question}

### Response:
"""


def split_documents(documents, chunk_size=1000, chunk_overlap=20):
    # Initializing the RecursiveCharacterTextSplitter with
    # chunk_size and chunk_overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # Splitting the documents into chunks
    chunks = text_splitter.split_documents(documents=documents)

    # returning the document chunks
    return chunks


# function for loading the embedding model
def load_embedding_model(model_path, normalize_embedding=True):
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={"device": "cpu"},  # here we will run the model with CPU only
        encode_kwargs={
            "normalize_embeddings": normalize_embedding  # keep True to compute cosine similarity
        },
    )

def create_ferret_embeddings(chunks):
    # Initialize Ferret model
    model_name = "TheBloke/Ferret_7B-GGUF"
    model_file = "ferret_7b.Q4_K_M.gguf"
    model_type = "mistral"
    llm = AutoModelForCausalLM.from_pretrained(model_name, model_file, model_type)

    # Encode each chunk with Ferret
    embeddings = [llm(chunk)["last_hidden_state"][:, 0, :] for chunk in chunks]

    return embeddings

# Function for creating embeddings using FAISS
def create_embeddings(chunks, embedding_model, storing_path="vectorstore2"):
    # Creating the embeddings using FAISS
    vectorstore = FAISS.from_documents(chunks, embe)

    # Saving the model in current directory
    vectorstore.save_local(storing_path)

    # returning the vectorstore
    return vectorstore


""" RetrievalQA does nott give chatbot memory i.e. It just \
answers your Questions\
but does nott memorise the previous conversations."""


# Creating the chain for Question Answering
def load_qa_chain(retriever, llm, prompt):
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,  # here we are using the vectorstore as a retriever
        chain_type="stuff",
        return_source_documents=True,  # including source documents in output
        chain_type_kwargs={"prompt": prompt},  # customizing the prompt
    )



# Prettifying the response
async def get_response(question, chain):
    # Getting response from chain
    response = chain({"query": question})

    # Wrapping the text for better output
    wrapped_text = textwrap.fill(response["result"], width=100)
    print(wrapped_text)
print("vector store is created")