import wave
import tempfile
import pyaudio
from pydub import AudioSegment
import whisper

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
p = pyaudio.PyAudio()

def recording():
    mic_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    print("Start recording...")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = mic_stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped.")

    mic_stream.stop_stream()
    mic_stream.close()
    p.terminate()

    # Recorded data is now stored in the 'frames' list
    recorded_data = b''.join(frames)
    return recorded_data
recorded_data = recording()   

def mp3_file_creator(recorded_data):
    temp_file_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    wave_file = wave.open(temp_file_path, 'wb')
    wave_file.setparams((CHANNELS, 2, RATE, 0, 'NONE', 'not compressed'))
    wave_file.writeframes(recorded_data)
    wave_file.close()


    audio = AudioSegment.from_wav(temp_file_path)

    # Export as MP3 with desired bitrate
    audio.export("output.mp3", format="mp3", bitrate="128k")
    model = whisper.load_model('base.en')
    text = model.transcribe('output.mp3',temperature = 0.0)
    print(text)
    return text

mp3_file_creator(recorded_data)