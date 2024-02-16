# using whisper openai model

import whisper
model = whisper.load_model('base')
result = model.transcribe('03_Work_Tasks_and_Responsibilities_-_Zapp_English_Vocabulary_for_Work_2.3.mp3')

print(result['text'])