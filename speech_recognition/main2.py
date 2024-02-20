import whisper
import speech_recognition
import numpy as np
# Load whisper model
model = whisper.load_model('base')

# Initialize the recognizer
r = speech_recognition.Recognizer()

# Continuously listen for audio
while True:
    try:
        with speech_recognition.Microphone() as source:
            print("recording started")
            # Adjust silence_threshold for noise sensitivity
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=10)
            print("recording completed")
        print(audio)
        # Transcribe the audio chunk
        audio = audio.astype(np.Float32)
        result = model.transcribe(audio)

        # Print the transcribed text
        print(result['text'])

    except KeyboardInterrupt:
        print("Transcription stopped.")
        break
