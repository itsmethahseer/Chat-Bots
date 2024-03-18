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






async def main():
    # Loading orca-mini from Ollama
    llm = Ollama(model="orca-mini", temperature=0)

    # Loading the Embedding Model
    embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

    # loading and splitting the documents
    docs = pdf_loader(
        file_path="/home/c847/Desktop/Chatbots with LLms/ollama_models/data/"
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

    while True:
        # Ask a question
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            break

        # Get and print the response incrementally
        response_generator = get_response_incremental(question, chain)
        async for partial_response in response_generator:
            print(partial_response)
            
async def get_response_incremental(question, chain):
    # Getting response from chain
    response = chain({"query": question})

    # Split the response into chunks
    chunks = response["result"].split("\n")

    for chunk in chunks:
        # Wrap the text for better output
        wrapped_chunk = textwrap.fill(chunk, width=100)
        yield wrapped_chunk
    await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
