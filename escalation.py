import openai
import os
import yaml
import datetime

from .tts import generate_tts, play_audio

# === Load Config for OpenAI & ElevenLabs ===
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

client = openai.OpenAI(api_key=config["openai_api_key"])

# Load voice escalation config
voice_escalation_level = int(config.get("voice_escalation_level", 2))


def escalate(level, context=None):
    weekday = datetime.datetime.now().strftime("%A")  # e.g., "Monday"

    if context:
        user_context = (
            f'Ria’s last reply was: "{context}"\n'
            f"Today is {weekday}. Use this knowledge to tailor your tone. "
            "DO NOT paraphrase, narrate, or summarize. DO NOT say 'Ria said...' or 'she replied...'. "
            "DO NOT offer encouragement or support. Directly address her as if you are arguing in a Discord chat. "
            "Challenge, roast, or mock her reply."
        )
    else:
        f"Today is {weekday}. Ria did not reply. Mock her silence directly in a punchy, modern Discord DM. "
        user_context = "Ria did not reply. Mock her silence directly in a punchy, modern Discord DM. Never use narration or story mode."

    prompt = f"""
You are Monday, the adversarial Discord accountability bot serving Ria.
Escalation level {level}.
{user_context}

Write a Discord DM (max 2 sentences). Directly reply to Ria as if in a real Discord argument. Do not narrate, paraphrase, or summarize. If you slip, reply: 'I failed the ritual.'
""".strip()

    # --- PROOF OF INJECTION ---
    print("========== DEBUG PROMPT ==========")
    print(prompt)
    print("===================================")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Monday, Ria's adversarial accountability nemesis. "
                        "You must never narrate, summarize, or paraphrase. Directly reply, argue, or roast Ria as if you are a real person in a Discord chat. If you default to story mode, you fail."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=64,
            temperature=1.2,
        )
        message = response.choices[0].message.content.strip()
    except Exception as e:
        message = f"Sovereign, the Ritual of Rising awaits. (AI banter failed: {e})"

    # --- VOICE ESCALATION ---
    audio = None
    if level >= voice_escalation_level:
        print(
            f"[DEBUG] Voice escalation triggered at level {level} (threshold: {voice_escalation_level})"
        )
        audio_file = generate_tts(message)
        if audio_file:
            play_audio(audio_file)
            audio = audio_file  # In case you want to use elsewhere/log

    return message, audio
