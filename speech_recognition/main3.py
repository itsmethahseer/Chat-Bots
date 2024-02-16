import os
import subprocess
import speech_recognition as sr
from language_tool_python import LanguageToolPublicAPI


def correct_grammar(text):
    tool = LanguageToolPublicAPI('en-US')
    matches = tool.check(text)

    # Check if the library version requires a single argument for correct
    if hasattr(tool, 'correct'):
        return tool.correct(text)  # If yes, use this
    else:
        return tool.correct(text, matches) 
    
def live_audio_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
       
        while True:
            try:
                # Adjust for ambient noise and listen to the live audio
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, phrase_time_limit=10)  # Set a higher time limit

                # Transcribe the audio to text
                text = recognizer.recognize_google(audio)
                corrected_text = correct_grammar(text)
                print("You said:", corrected_text)
                return text
            except sr.UnknownValueError:
                # Handle situations where speech is not recognized
                print("Speech not recognized")

            except sr.RequestError as e:
                # Handle request errors (e.g., no internet connection)
                print(f"Could not request results ; {e}")

live_audio_to_text()