import requests
import yaml

with open("accountability_bot/config.yaml") as f:
    config = yaml.safe_load(f)

API_KEY = config["elevenlabs_api_key"]


def generate_tts(text, filename="reminder.mp3"):
    url = "https://api.elevenlabs.io/v1/text-to-speech/your_voice_id"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        print("Failed to generate TTS:", response.text)
        return None
