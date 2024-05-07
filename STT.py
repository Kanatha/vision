import whisper
import pyaudio
import numpy as np

# Function to process audio chunks
def process_audio_chunk(chunk):
    # Convert chunk to Mel spectrogram
    mel = whisper.log_mel_spectrogram(chunk).to(model.device)

    # Decode the audio chunk
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # Print the recognized text
    print(result.text)

# Load the model
model = whisper.load_model("base")

# Initialize PyAudio
chunk_size = 1024
sample_rate = 44100
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

print("Starting transcription...")

# Continuously stream audio and process it in real-time
try:
    while True:
        # Read audio chunk
        chunk = np.frombuffer(stream.read(chunk_size), dtype=np.int16)

        # Process the audio chunk
        process_audio_chunk(chunk)
except KeyboardInterrupt:
    print("Stopping transcription...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
