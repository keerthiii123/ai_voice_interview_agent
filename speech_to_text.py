import os

from deepgram import DeepgramClient
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


def transcribe_audio(audio_bytes):

    if not DEEPGRAM_API_KEY:
        raise ValueError(
            "DEEPGRAM_API_KEY is not configured."
        )

    try:

        print("Sending audio to Deepgram...")

        client = DeepgramClient(
            DEEPGRAM_API_KEY
        )

        response = client.listen.rest.v("1").transcribe_file(
            {
                "buffer": audio_bytes
            },
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

        if not text or not text.strip():
            return "No speech detected."

        return text.strip()

    except Exception as e:

        print("Deepgram Error:", e)

        raise Exception(
            f"Speech-to-Text Error: {e}"
        )