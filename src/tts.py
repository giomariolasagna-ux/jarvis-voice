from openai import OpenAI
import tempfile
import subprocess
import os
import time

client = OpenAI()

VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
vlc_process = None

def stop_speaking():
    global vlc_process
    if vlc_process and vlc_process.poll() is None:
        vlc_process.kill()
        vlc_process = None

def speak(text):
    global vlc_process

    if not text or not text.strip():
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        audio_path = f.name

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts-2025-03-20",
        voice="alloy",
        input=text
    ) as r:
        r.stream_to_file(audio_path)

    # avvio VLC NON bloccante
    vlc_process = subprocess.Popen(
        [
            VLC_PATH,
            "--intf", "dummy",
            "--play-and-exit",
            audio_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # aspetta che finisca
    vlc_process.wait()

    vlc_process = None
    time.sleep(0.2)

    if os.path.exists(audio_path):
        os.remove(audio_path)
