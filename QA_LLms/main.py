import streamlit as st
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from transformers import MarianTokenizer, MarianMTModel, GPT2Tokenizer, GPT2LMHeadModel
import os
from api import Hugging_face
os.environ['HUGGINGFACEHUB_API_TOKEN'] = Hugging_face
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
# Initialize the HuggingFaceHub
llm = HuggingFaceHub()

# Create a list of task options
task_options = ["Question Answering", "Language Translation"]

# Create a radio button to select the task
st.title("Tava App")
selected_task = st.radio("Select a task:", task_options)


def generate_content(topic, word_count):
    # Generate content using the GPT-2 model
    prompt = f"Write an informative piece about {topic}."
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    # Generate text continuation with adjusted parameters
    output = model.generate(input_ids, max_length=word_count + len(input_ids[0]), temperature=0.8, top_k=50)
    
    # Decode the generated output
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return generated_text

# Logic for the selected task
if selected_task == "Question Answering":
    # Question Answering Logic
    template = """Question: {question}\n\nAnswer: Let's think step by step."""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    repo_id = "google/flan-t5-xxl"
    llm_instance = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 500}
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm_instance)
    
    question = st.text_input("Enter a question:", "")
    if question:
        generated_text = llm_chain.run(question)
        st.subheader("Generated Text:")
        st.write(generated_text)

elif selected_task == "Language Translation":
    # Language Translation Logic
    source_text = st.text_area("Enter the source text:", "")
    target_language = st.selectbox("Select target language:", ["de", "es", "fr","ml"])  # Language codes
    
    if source_text:
        model_name = f"Helsinki-NLP/opus-mt-en-{target_language}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        input_ids = tokenizer.encode(source_text, return_tensors="pt")
        translated_ids = model.generate(input_ids, max_length=128, num_beams=4, early_stopping=True)
        translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        
        st.subheader("Translated Text:")
        st.write(translated_text)