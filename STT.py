from flask import Flask, render_template, request
from faster_whisper import WhisperModel
import os
import requests
import json
import tts

app = Flask(__name__)

# Initialize the model outside of the route functions
model_size = "tiny"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# Chatbot API URL
chatbot_api_url = "http://localhost:11434/api/chat"

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

        print("Transcribed text:")
        print(transcribed_text)

        # Make a request to the chatbot API
        payload = {
            "model": "llama3",  # Update with the appropriate model name
            "messages": [{
                "role": "user",
                "content": transcribed_text.split('] ')[-1]  # Pass transcribed text to the chatbot
            }],
            "stream": False,
            "keep_alive": -1
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(chatbot_api_url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            try:
                returned_json = response.json()
                message = returned_json.get("message", {})
                content = message.get("content", "")
                print("Chatbot response:")
                print(content)
                tts.play_text_as_audio(content)
            except json.JSONDecodeError as e:
                print("Error decoding JSON response: " + str(e))
        else:
            print("Error: " + str(response.status_code) + " " + response.text)

        return 'Audio transcribed successfully and chatbot response printed to console.'

    finally:
        # Ensure the file is closed before deletion
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
            print("File deleted.")

if __name__ == '__main__':
    app.run(debug=True)
