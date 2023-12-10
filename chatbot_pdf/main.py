import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from template import css, bot_template, user_template
from langchain.llms import HuggingFaceHub, CTransformers

DB_FAISS_PATH = 'Vectorstore/db_faiss'

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
            
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(separator="\n",
                                          chunk_size=1000,
                                          chunk_overlap=200,
                                          length_function=len)
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                   model_kwargs={'device':'cpu'})
    vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

def get_demo_vectorstore(DB_FAISS_PATH):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                   model_kwargs={'device':'cpu'})
    vectorstore = FAISS.load_local(DB_FAISS_PATH, embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(memory_key='chat_history',return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vectorstore.as_retriever(),
        memory=memory 
    )
    return conversation_chain
    
def handle_userinput(user_question):
    response = st.session_state.conversation({'question':user_question})
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i%2==0:
            st.write(user_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)
    

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with pdfs")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
        
    st.header("Chat with pdfs")
    
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your pdfs here",accept_multiple_files=True)
        st.markdown("**If you don't have a PDF to upload, just press 'Process'. It has data based on the [Constitution_BillOfRights.pdf](https://www.constitutionfacts.com/content/constitution/files/Constitution_BillOfRights.pdf)**")
        if st.button("Process"):
            with st.spinner("Processing"):
                if len(pdf_docs) ==0 :
                    demo_vectorstore = get_demo_vectorstore(DB_FAISS_PATH)
                    st.session_state.conversation = get_conversation_chain(demo_vectorstore)
                else:
                    raw_text = get_pdf_text(pdf_docs)
                    
                    text_chunks = get_text_chunks(raw_text)
                    
                    vectorstore = get_vectorstore(text_chunks)

                    st.session_state.conversation = get_conversation_chain(vectorstore)
                
    user_question = st.text_input("Enter the questions",placeholder="Example: What is the first amendment?")
    if user_question:
        handle_userinput(user_question)
        
        
                
if __name__ == '__main__':
    main()