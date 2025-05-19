import requests
import yaml
import os
import subprocess

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

API_KEY = config["elevenlabs_api_key"]
VOICE_ID = config["voice_id"]
MODEL_ID = config.get(
    "voice_model_id", "eleven_monolingual_v1"
)  # Optional, default model


def generate_tts(text, filename="reminder.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {"stability": 0.7, "similarity_boost": 0.75},
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"[DEBUG] TTS file generated: {filename}")
        return filename
    else:
        print("[ERROR] Failed to generate TTS:", response.text)
        return None


def play_audio(filename="reminder.mp3"):
    try:
        subprocess.run(["mpv", filename], check=True)
        print(f"[DEBUG] Playing audio file: {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to play audio: {e}")


# Example usage:
if __name__ == "__main__":
    import sys

    text = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "The ritual has begun, Sovereign."
    )
    audio_file = generate_tts(text)
    if audio_file:
        play_audio(audio_file)
