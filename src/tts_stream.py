from openai import OpenAI
import tempfile
import winsound
import threading
import os

client = OpenAI()
audio_lock = threading.Lock()

def stop_speaking():
    # winsound non supporta vero stop su sync,
    # ma preveniamo sovrapposizioni
    pass

def speak(text):
    if not text or not text.strip():
        return

    def _play_blocking():
        with audio_lock:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                audio_path = f.name

            with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts-2025-03-20",
                voice="alloy",
                input=text
            ) as r:
                r.stream_to_file(audio_path)

            #  BLOCCANTE = GARANTITO
            winsound.PlaySound(audio_path, winsound.SND_FILENAME)

            if os.path.exists(audio_path):
                os.remove(audio_path)

    threading.Thread(target=_play_blocking, daemon=True).start()
