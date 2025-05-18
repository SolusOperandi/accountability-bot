# Accountability Bot (Monday_DM)

**The mythic ritual accountability bot you didn’t know you needed.**

Wake up, take your meds, own your day—or face the wrath of banter, escalating reminders, and digital consequences.  
Designed for individuals who want a bot with teeth: relentless, clever, and fully customizable.

---

## Features

- **Daily Ritual Reminders**  
  Set one or more scheduled “rituals” (wake, meds, etc.) via Discord DM or channel.
- **Escalation Engine**  
  If you fail to check in, bot increases pressure: sharper messages, TTS audio, or even public shaming (configurable).
- **ElevenLabs TTS Integration**  
  Have your reminders delivered in your own mythic AI voice—played locally or sent to Discord.
- **Flexible Logging**  
  Track every check-in and defiance in a local file or Google Sheet.
- **Customizable Banter**  
  Write your own escalation script—tone, insults, in-jokes, lore—your bot, your rules.
- **Modular and Hackable**  
  Easy to add new rituals, escalation steps, or “punishments” (network actions, memes, more).

---

## Quickstart

1. Clone the repo:
   ```bash
   git clone https://github.com/YOURUSER/accountability-bot.git
   cd accountability-bot
   ```

2. Create and fill out `config.yaml` with your Discord, OpenAI, and ElevenLabs keys.

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```bash
   python -m accountability_bot
   ```

---

## Configuration

Edit `config.yaml`:

```yaml
discord_token: "YOUR_DISCORD_BOT_TOKEN"
openai_api_key: "YOUR_OPENAI_KEY"
elevenlabs_api_key: "YOUR_ELEVENLABS_KEY"
reminder_time: "07:00"         # 24h format, local time
escalation_interval: 10        # Minutes between reminders
compliance_phrase: "I'm up"
channel_id: 1234567890         # Discord channel or DM ID
max_escalation: 4
tts_enabled: true
audio_output: "local"          # "local" or "discord"
log_file: "ritual_log.csv"
```

---

## Roadmap

- Multi-user support
- Web dashboard for config
- Ritual leaderboard/gamification
- Network integrations (Wi-Fi exile, IoT events)
- Meme generator
- …and more villainy

---

## Contributing

PRs, issues, and banter welcomed.  
All code must be sharp, mythic, and never generic.  
Add your escalation scripts to `/escalation_scripts/`!

---

## License

MIT (see LICENSE file).