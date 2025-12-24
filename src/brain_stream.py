from src.moonshot_stream import stream_moonshot

MIN_CHARS = 120   # più naturale per parlato
MAX_CHARS = 220   # evita monologhi infiniti

def jarvis_brain_stream(user_text):
    messages = [
        {
            "role": "system",
            "content": (
                "Sei Jarvis, assistente vocale mentre lutente lavora al computer. "
                "Parla in modo naturale, con frasi complete e ritmo umano."
            )
        },
        {"role": "user", "content": user_text}
    ]

    buffer = ""

    for token in stream_moonshot(messages):
        buffer += token

        # 1 frase completa
        if any(p in buffer for p in [".", "?", "!"]) and len(buffer) >= MIN_CHARS:
            yield buffer.strip()
            buffer = ""
            continue

        # 2 chunk lungo ma senza punteggiatura
        if len(buffer) >= MAX_CHARS and buffer.endswith(" "):
            yield buffer.strip()
            buffer = ""

    if buffer.strip():
        yield buffer.strip()
