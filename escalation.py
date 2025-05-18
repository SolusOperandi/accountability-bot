def escalate(level):
    # Replace these with your own mythic/roast messages
    messages = [
        "Sovereign, the Ritual of Rising begins. Will you rise, or will the day shame you again?",
        "Still slumbering? The world is unimpressed.",
        "This is your third warning. Get up, or I'll start reciting your browser history.",
        "Final call: If you don't rise now, your legend ends here—public roast commencing.",
    ]
    audios = [
        None,  # Optional: Path to TTS file generated
        None,
        None,
        None,
    ]
    return (
        messages[min(level - 1, len(messages) - 1)],
        audios[min(level - 1, len(audios) - 1)],
    )
