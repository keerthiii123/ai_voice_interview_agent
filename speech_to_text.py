import os
import wave
import numpy as np
import sounddevice as sd
from deepgram import DeepgramClient, FileSource
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 10
AUDIO_FILE = "candidate_answer.wav"


def record_audio():

    print("=" * 60)
    print("MICROPHONE")
    print("=" * 60)

    print(f"Sample Rate: {SAMPLE_RATE} Hz")
    print(f"Duration   : {DURATION} seconds")

    print("\nRecording started...")
    print("Please speak clearly...")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    )

    for i in range(DURATION):
        sd.sleep(1000)
        print(f"Recording... {i + 1}/{DURATION}s")

    sd.wait()

    print("Recording stopped.")

    # ---------------------------------------------------------
    # CHECK AUDIO LEVEL
    # ---------------------------------------------------------

    max_volume = float(np.max(np.abs(audio)))
    average_volume = float(np.mean(np.abs(audio)))

    print(f"\nMax volume     : {max_volume:.6f}")
    print(f"Average volume : {average_volume:.6f}")

    if max_volume < 0.005:
        print("WARNING: Very low microphone volume.")

    # ---------------------------------------------------------
    # NORMALIZE AUDIO
    # ---------------------------------------------------------

    if max_volume > 0:

        audio = audio / max_volume

        # Prevent clipping
        audio = audio * 0.8

    audio_int16 = (audio * 32767).astype(np.int16)

    # ---------------------------------------------------------
    # SAVE WAV
    # ---------------------------------------------------------

    with wave.open(AUDIO_FILE, "wb") as wf:

        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)

        wf.writeframes(audio_int16.tobytes())

    print(f"Audio saved: {AUDIO_FILE}")


def transcribe_audio():

    print("\nSending audio to Deepgram...")

    try:

        client = DeepgramClient(DEEPGRAM_API_KEY)

        with open(AUDIO_FILE, "rb") as audio:

            buffer_data = audio.read()

        payload: FileSource = {
            "buffer": buffer_data
        }

        response = client.listen.rest.v("1").transcribe_file(
            payload,
            {
                "model": "nova-3",
                "language": "en-IN",
                "smart_format": True,
                "punctuate": True,
                "diarize": False
            }
        )

        text = (
            response
            .results
            .channels[0]
            .alternatives[0]
            .transcript
        )

        print("\n" + "=" * 60)
        print("YOU SAID")
        print("=" * 60)

        if not text or not text.strip():

            text = "No speech detected."

        print(text)

        print("=" * 60)

        return text.strip()

    except Exception as e:

        print("\nDeepgram Error:")
        print(e)

        return "No speech detected."


def speech_to_text():

    record_audio()

    return transcribe_audio()


if __name__ == "__main__":

    print("=" * 60)
    print("AI VOICE INTERVIEW - SPEECH TO TEXT TEST")
    print("=" * 60)

    result = speech_to_text()

    print("\nReturned text:")
    print(result)

    print("\nTEST COMPLETED")