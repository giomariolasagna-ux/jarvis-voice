import threading
_MIC_LOCK = threading.Lock()
from openai import OpenAI
import sounddevice as sd
import soundfile as sf
import tempfile
import os
import numpy as np
import queue

client = OpenAI()

SAMPLE_RATE = 16000
CHANNELS = 1

#  BLOCCO PER NOME (NON PER INDICE)
TARGET_NAME = "LifeCam"

def find_mic():
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0 and TARGET_NAME in d["name"]:
            return i, d
    raise RuntimeError("Microfono LifeCam non trovato")

MIC_INDEX, DEVICE_INFO = find_mic()
REAL_CHANNELS = DEVICE_INFO["max_input_channels"]

print(f" Using device: {DEVICE_INFO['name']} | Channels: {REAL_CHANNELS}")

def record_while_pressed(is_recording_fn):
    if not _MIC_LOCK.acquire(blocking=False):
        print("Microfono già in uso, skip recording")
        return None

    q = queue.Queue()
    frames = []

    def callback(indata, frames_count, time, status):
        if status:
            print(status)
        q.put(indata.copy())

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=REAL_CHANNELS,
        device=MIC_INDEX,
        callback=callback
    ):
        while is_recording_fn():
            try:
                frames.append(q.get(timeout=0.1))
            except queue.Empty:
                continue

    if not frames:
        return None

    audio = np.concatenate(frames, axis=0)

    #  DOWNMIX A MONO
    if REAL_CHANNELS > 1:
        audio = np.mean(audio, axis=1, keepdims=True)

    level = abs(audio).mean()
    print(f" Audio level: {level:.6f}")

    if level < 0.001:
        print(" Audio troppo basso / silenzio")
        return None

    _MIC_LOCK.release()
    return audio

def transcribe_audio(audio):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        sf.write(f.name, audio, SAMPLE_RATE)
        path = f.name

    with open(path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe-2025-03-20",
            file=audio_file
        )

    os.remove(path)
    return result.text

