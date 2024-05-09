from flask import Flask, render_template, request
from faster_whisper import WhisperModel
import os

app = Flask(__name__)

# Initialize the model outside of the route functions
model_size = "tiny"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

@app.route('/')
def index():
    return render_template('audiorec.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Receive audio data from the frontend
    audio_data = request.files['audio_data']
    # Save the audio data to a file or process it further
    audio_file_path = 'recorded_audio.wav'

    try:
        with open(audio_file_path, 'wb') as f:
            f.write(audio_data.read())

        # Use the initialized model for transcription
        segments, info = model.transcribe(audio_file_path, beam_size=5)

        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        transcribed_text = ""
        for segment in segments:
            transcribed_text += "[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text)

        print(transcribed_text)

        return 'Audio transcribed successfully:\n' + transcribed_text

    finally:
        # Ensure the file is closed before deletion
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
            print("File deleted.")

if __name__ == '__main__':
    app.run(debug=True)
