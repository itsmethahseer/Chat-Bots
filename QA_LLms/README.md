# Tava App

## Overview

Tava App is a mini-project that leverages large language models for question answering and language translation. It provides users with the ability to interact with two powerful functionalities:

1. **Question Answering:** Utilizing the Google/Flax-T5-XXL model, Tava App enables users to input questions and receive accurate answers.

2. **Language Translation:** Powered by the Helsinki-NLP/opus-mt-en-{target_language} model, the app allows users to translate text between English and various target languages, including Malayalam, French, and more.

## Features

- **Question Answering:**
  - Enter a question in English, and the app will provide a detailed answer.
  
- **Language Translation:**
  - Translate text from English to various target languages and vice versa.

## Usage

1. Clone the repository to your local machine.

```bash
git clone https://github.com/your_username/Tava-App.git
```

2. Install the required dependencies.

```bash
pip install -r requirements.txt
```

3. Run the application.

```bash
python myapp.py
```


## How to Interact

- **Question Answering:**
  - Enter your question in the provided input box.
  - The app will return the answer generated by the Google/Flax-T5-XXL model.

- **Language Translation:**
  - Select the target language from the dropdown menu.
  - Enter the text you want to translate in the provided input box.
  - The translated text will be displayed below.

## Models Used

- **Question Answering:**
  - [Google/Flax-T5-XXL](https://huggingface.co/google/flax-t5-xxl)

- **Language Translation:**
  - [Helsinki-NLP/opus-mt-en-{target_language}](https://huggingface.co/Helsinki-NLP/opus-mt-en-mal)

## Example
![Screenshot 2023-09-11 154008](https://github.com/itsmethahseer/Tava-App/assets/120078997/975c77df-b172-469d-9204-5d73ee804ddb)

![Screenshot 2023-09-11 154104](https://github.com/itsmethahseer/Tava-App/assets/120078997/b70508d2-d2e5-4d03-b820-15639e9bea6f)
- **Question Answering:**

  Input: "What is the capital of France?"

  Output: "Paris"

- **Language Translation:**

  English to Malayalam

  Input: "Hello, how are you?"

  Output: "ഹലോ, സുഖമാണോ?"

## Folder Structure

- `.ipynb_checkpoints/`: Checkpoints for Jupyter Notebooks.
- `__pycache__/`: Cached Python files.
- `venv/`: Virtual environment for the project.
- `LLM_Project.ipynb`: Jupyter Notebook contains another LLM Models workouts.
- `myapp2.py`: Contains two large language models for question answering and language translation.

## Contributions

Contributions are welcome! If you'd like to improve this project, please create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to add more sections or customize this README file as per your specific needs. Good luck with your Tava App!