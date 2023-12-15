# Chatbot Suite

Welcome to the Chatbot Suite project, a collection of diverse chatbots for various purposes, including question answering, language translation, and document-based interactions. Each chatbot leverages state-of-the-art language models and technologies to provide unique functionalities.


## Directory Structure

The project is organized into several directories, each housing a distinct chatbot application:

1. **QA_LLms:** Implements a chatbot capable of question answering and language translation. Utilizes Google/Flax-T5-XXL for question answering and Helsinki-NLP/opus-mt-en-{target_language} for language translation.

2. **pdf_chatbot:** Contains a chatbot application for question answering from documents, such as PDFs. Utilizes Google/Flan-T5-XXL from Huggingface and employs faiss for embedding-related processes. The implementation is integrated into the langchain library.

3. **llama2chatbot:** Implements a chatbot using the llama2 pre-trained model. Offers enhanced text generation for question answering from documents. Utilizes Pinecone vector database for efficient processing.

4. **ollama_models:** Includes a chatbot for document-based question answering using the ollama class's fine-tuned model named orca-mini. Offers lower memory usage compared to llama2.

5. **GenerativeAI:** Utilizes Google's palm model to create a chatbot for various conversational purposes.

## Chatbot Descriptions

1. **QA_LLms:**
   - **Capabilities:** Question answering, language translation.
   - **Models:** Google/Flax-T5-XXL, Helsinki-NLP/opus-mt-en-{target_language}.

2. **pdf_chatbot:**
   - **Capabilities:** Document-based question answering, PDF interaction.
   - **Model:** Google/Flan-T5-XXL.
   - **Libraries:** Langchain, faiss.

3. **llama2chatbot:**
   - **Capabilities:** Enhanced text generation for question answering.
   - **Model:** llama2 pre-trained model.
   - **Database:** Pinecone vector.

4. **ollama_models:**
   - **Capabilities:** Document-based question answering with low memory usage.
   - **Model:** orca-mini.

5. **GenerativeAI:**
   - **Capabilities:** Conversational chatbot using Google's palm model.

## Usage

Created a Vectorstore of Google vertex AI, and stored the embeddings in it. Finally used a Palm Predictor client to predict the output of the question. 

## Dependencies

The project relies on the following dependencies:
- Python 3.x
- [Huggingface Transformers](https://github.com/huggingface/transformers)
- [Langchain Library](https://www.langchain.com/)
- [Faiss](https://github.com/facebookresearch/faiss)
- [Pinecone](https://www.pinecone.io/)

For specific dependencies of each chatbot, refer to the README file in the respective directory.

## Contributing

We welcome contributions to enhance and expand the capabilities of our chatbots. Feel free to submit issues, feature requests, or pull requests.

## Acknowledgments

We appreciate the contributions of the open-source community and the developers behind the libraries and models used in this project.

## Research and Future Development

Actively researching new technologies and enhancements for future iterations. Stay tuned for updates and exciting developments in the field of conversational AI.
