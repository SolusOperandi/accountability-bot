import discord
import asyncio
import yaml
import datetime
from .escalation import escalate
from .logger import log_ritual

with open("accountability_bot/config.yaml") as f:
    config = yaml.safe_load(f)

TOKEN = config["discord_token"]
CHANNEL_ID = config["channel_id"]
REMINDER_TIME = config["reminder_time"]
ESCALATION_INTERVAL = config["escalation_interval"]
MAX_ESCALATION = config["max_escalation"]
COMPLIANCE_PHRASE = config["compliance_phrase"]

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

compliant = asyncio.Event()


async def send_reminder(escalation_level):
    message, audio = escalate(escalation_level)
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(message)
    if audio:
        # Local playback or attach to message
        pass


async def ritual_loop():
    await client.wait_until_ready()
    while True:
        now = datetime.datetime.now()
        ritual_time = datetime.datetime.strptime(REMINDER_TIME, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if now > ritual_time:
            ritual_time = ritual_time + datetime.timedelta(days=1)
        delay = (ritual_time - now).total_seconds()
        await asyncio.sleep(delay)
        compliant.clear()
        for level in range(1, MAX_ESCALATION + 1):
            await send_reminder(level)
            try:
                await asyncio.wait_for(compliant.wait(), ESCALATION_INTERVAL * 60)
                log_ritual(True, level)
                break
            except asyncio.TimeoutError:
                continue
        else:
            log_ritual(False, MAX_ESCALATION)
            # Optional: perform ultimate punishment here


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.strip().lower() == COMPLIANCE_PHRASE.lower():
        compliant.set()


async def start_bot():
    client.loop.create_task(ritual_loop())
    await client.start(TOKEN)
