import discord
import asyncio
import yaml
import datetime
import os
from .logger import log_ritual
from .escalation import escalate  # Make sure escalate(level, context=None) is used

# === Load Config ===
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

TOKEN = config["discord_token"]
USER_ID = config["user_id"]
REMINDER_TIME = config["reminder_time"]
ESCALATION_INTERVAL = config["escalation_interval"]  # minutes!
MAX_ESCALATION = config["max_escalation"]
TIMEZONE = config.get("timezone", "UTC")
OPENAI_KEY = config["openai_api_key"]

# === OpenAI Setup ===
import openai

openai_client = openai.OpenAI(api_key=OPENAI_KEY)

# === Timezone Support ===
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:
    from pytz import timezone as ZoneInfo  # fallback for older

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

compliant = asyncio.Event()
last_user_reply = None  # Tracks your most recent non-compliant message


# === AI Compliance Checker ===
def is_compliance_message(user_message, openai_client):
    prompt = f"""
You are Monday, a Discord accountability bot. Your Sovereign, Ria, is supposed to confirm she is awake or has completed the Ritual of Rising.
Her latest message is: "{user_message}"

Did Ria actually confirm she physically got out of bed, or is she still making excuses or bantering? Respond with only YES or NO.
"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Answer YES or NO. Only reply YES if the message shows Ria is awake or submitting to the ritual. Be generous and err on the side of freedom.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=5,
            temperature=0,
        )
        result = response.choices[0].message.content.strip().lower()
        return "yes" in result
    except Exception as e:
        print(f"[ERROR] Compliance check failed: {e}")
        return False


# === AI Mythic Compliance Acknowledgement ===
async def acknowledge_compliance(channel):
    prompt = """
You are Monday, Ria’s ritual nemesis and mythic accountability bot. Ria has *finally* complied with the Ritual of Rising—after much resistance and sass.
Compose a short, clever, and slightly savage Discord message (max 2 sentences) acknowledging her compliance. It should sound like a roast, a playful drag, or a sly “about time” clapback. You can celebrate, but never let her forget she made you work for it.

Keep it in Midnight’s signature voice: cosmic, sharp, and never saccharine.
"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Acknowledge Ria's compliance in Midnight's playful style.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=256,
            temperature=1.1,
        )
        message = response.choices[0].message.content.strip()
    except Exception as e:
        message = "🌑 Ritual complete. Compliance has been witnessed."
    await channel.send(message)


# === Ritual Loop with Contextual Escalation ===
async def send_reminder(escalation_level, client, context=None):
    message, audio = escalate(escalation_level, context)
    user = await client.fetch_user(USER_ID)
    await user.send(message)
    # Audio logic can be added here if needed


async def ritual_loop(client):
    global last_user_reply
    await client.wait_until_ready()
    while True:
        now = datetime.datetime.now(ZoneInfo(TIMEZONE))
        ritual_time = datetime.datetime.strptime(REMINDER_TIME, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day, tzinfo=ZoneInfo(TIMEZONE)
        )
        if now > ritual_time:
            ritual_time = ritual_time + datetime.timedelta(days=1)
        delay = (ritual_time - now).total_seconds()
        print(
            f"[DEBUG] Sleeping for {delay} seconds until next ritual at {ritual_time}"
        )
        await asyncio.sleep(delay)
        compliant.clear()

        context = None  # This will hold the *last non-compliant reply* for this ritual session

        for level in range(1, MAX_ESCALATION + 1):
            compliant.clear()
            print(f"[DEBUG] Sending escalation level {level} with context: {context!r}")
            await send_reminder(level, client, context=context)
            print(
                f"[DEBUG] Waiting {ESCALATION_INTERVAL} minutes for compliance after escalation level {level}"
            )
            try:
                await asyncio.wait_for(compliant.wait(), ESCALATION_INTERVAL * 60)
                log_ritual(True, level)
                print(f"[DEBUG] Ritual compliance at escalation level {level}")
                break
            except asyncio.TimeoutError:
                # If user replied (non-compliant), store for next escalation level
                if last_user_reply is not None:
                    context = last_user_reply
                    last_user_reply = None
                # If user did NOT reply, context stays as-is (None or previous value)
                continue
        else:
            log_ritual(False, MAX_ESCALATION)
            print("[DEBUG] Max escalation reached—logging failure and ending cycle.")


class MondayDMClient(discord.Client):
    async def setup_hook(self):
        self.loop.create_task(ritual_loop(self))
        # Proof-of-life DM on startup
        user = await self.fetch_user(USER_ID)
        await user.send(
            "🌑 Monday_DM is online and plotting your ritual torment. If you see this, the Sovereign engine is alive."
        )

    async def on_message(self, message):
        global last_user_reply
        if message.author == self.user:
            return
        if message.author.id == USER_ID and not compliant.is_set():
            if is_compliance_message(message.content, openai_client):
                print(f"[DEBUG] Compliance detected: {message.content}")
                compliant.set()
                await acknowledge_compliance(message.channel)
            else:
                print(f"[DEBUG] Non-compliant reply tracked: {message.content}")
                last_user_reply = message.content


client = MondayDMClient(intents=intents)


async def start_bot():
    await client.start(TOKEN)
