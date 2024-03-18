import wave
import tempfile
import pyaudio
from pydub import AudioSegment
import whisper
import time
import threading
import os 
import pyttsx3

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10

def start_recording(frames):
    p = pyaudio.PyAudio()
    try:
        mic_stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
        print("Recording started.")
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = mic_stream.read(CHUNK)
            frames.append(data)
        print("Recording stopped.")
        return True
    except Exception as e:
        print(f"Error during recording: {e}")
        return False
    finally:
        mic_stream.stop_stream()
        mic_stream.close()
        p.terminate()

def transcribe_audio(audio_file):
    try:
        model = whisper.load_model('base.en')
        text = model.transcribe(audio_file,temperature = 0.0)
        return text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def record_and_transcribe():
    frames = []
    recording_thread = threading.Thread(target=start_recording, args=(frames,))
    recording_thread.start()
    recording_thread.join()  # Wait for recording to finish

    if recording_thread.is_alive():
        print("Recording timed out.")
        return {"error": "Recording timed out"}

    try:
        temp_file_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        with wave.open(temp_file_path, 'wb') as wave_file:
            wave_file.setparams((CHANNELS, 2, RATE, 0, 'NONE', 'not compressed'))
            wave_file.writeframes(b''.join(frames))

        audio = AudioSegment.from_wav(temp_file_path)
        audio.export("output.mp3", format="mp3", bitrate="128k")

        transcription = transcribe_audio("output.mp3")
        result = text_to_speech(transcription['text'])
        print(transcription,'transcription')
        return transcription['text'] and result
    finally:
        # Clean up temporary files
        try:
            os.remove(temp_file_path)
            os.remove("output.mp3")
        except Exception:
            pass
        
        
def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)    # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Convert text to speech
    engine.say(text)
    engine.runAndWait()
    

record_and_transcribe()