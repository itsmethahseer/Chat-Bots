import asyncio
import textwrap
import openai
from main import (
    load_embedding_model,
    create_embeddings,
    load_qa_chain,
    split_documents,
    pdf_loader,
    template,
)
from langchain.llms.ollama import Ollama
from langchain.prompts import PromptTemplate

# Set your OpenAI API key
openai.api_key = "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"

async def main():
    # Loading orca-mini from Ollama
    llm = Ollama(model="orca-mini", temperature=0)

    # Loading the Embedding Model
    embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

    # loading and splitting the documents
    docs = pdf_loader(
        file_path="/home/c847/Desktop/Chatbots with LLms/ollama_models/data/cricket.pdf"
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

        # Use the OpenAI API to get a response
        async with openai.Completion.create(
            model="text-davinci-003",  # or another available GPT-3 model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            stream=True,
        ) as response:
            for message in response.choices:
                if message.role == "assistant":
                    content = message.content
                    # Split the response into chunks
                    chunks = content.split("\n")
                    for chunk in chunks:
                        # Wrap the text for better output
                        wrapped_chunk = textwrap.fill(chunk, width=100)
                        print(wrapped_chunk)
                        await asyncio.sleep(0.5)


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
