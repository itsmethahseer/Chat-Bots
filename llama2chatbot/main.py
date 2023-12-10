env_of_index = "gcp-starter"
api_key_pinecone = "api token of your pincone"
api_token_for_my_github = "api token for your github"

import os
import sys
import pinecone
from langchain.llms import Replicate
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain



# Replicate API token
os.environ['REPLICATE_API_TOKEN'] = api_token_for_my_github


# Initialize Pinecone
pinecone.init(api_key=api_key_pinecone, environment=env_of_index)


# Load and preprocess the PDF document
loader = PyPDFLoader('./alzheimers-dementia-about-alzheimers-disease-ts.pdf')
documents = loader.load()

# Split the documents into smaller chunks for processing
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)


# Use HuggingFace embeddings for transforming text into numerical vectors
embeddings = HuggingFaceEmbeddings()

# Set up the Pinecone vector database
index_name = "myintex"
index = pinecone.Index(index_name)
vectordb = Pinecone.from_documents(texts, embeddings, index_name=index_name)

# Initialize Replicate Llama2 Model
llm = Replicate(
    model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
    model_kwargs={"temperature": 0.75, "max_length": 3000}
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    vectordb.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True
)

# Start chatting with the chatbot
chat_history = []
while True:
    query = input('Prompt: ')
    if query.lower() in ["exit", "quit", "q"]:
        print('Exiting')
        sys.exit()

    request = {
        "question": query,
        "chat_history": chat_history
    }

    result = qa_chain(request)
    print('Answer: ' + result['answer'] + '\n')
    chat_history.append((query, result['answer']))

    

        
