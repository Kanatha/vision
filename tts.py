import requests
import pygame
from io import BytesIO

# Initialize Pygame
pygame.init()

def play_audio_from_url(url):
    # Fetch audio data from URL
    response = requests.get(url)
    if response.status_code == 200:
        # Load audio data into pygame mixer
        audio_data = BytesIO(response.content)
        pygame.mixer.music.load(audio_data)
        # Play audio
        pygame.mixer.music.play()
        # Wait until audio is finished playing
        while pygame.mixer.music.get_busy():
            continue
    else:
        print("Failed to fetch audio from URL")

def play_text_as_audio(text):
    # Construct URL with text parameter
    base_url = "http://localhost:5500/api/tts"
    parameters = {
        "voice": "nanotts:en-GB",
        "text": text,
        "denoiserStrength": "0.03",
        "cache": "false"
    }
    url = base_url + "?" + "&".join([f"{key}={value}" for key, value in parameters.items()])
    
    # Play audio from constructed URL
    play_audio_from_url(url)

if __name__ == "__main__":
    text = "Welcome to the world of speech synthesis!"
    play_text_as_audio(text)
