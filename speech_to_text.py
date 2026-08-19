import os
from deepgram import DeepgramClient
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


def transcribe_audio(audio_bytes):

    try:

        if not DEEPGRAM_API_KEY:
            return "Deepgram API key not configured."

        client = DeepgramClient(DEEPGRAM_API_KEY)

        payload = {
            "buffer": audio_bytes
        }

        options = {
            "model": "nova-3",
            "language": "en-IN",
            "smart_format": True,
            "punctuate": True
        }

        response = client.listen.rest.v1.transcribe_file(
            payload,
            options
        )

        text = (
            response
            .results
            .channels[0]
            .alternatives[0]
            .transcript
        )

        if not text.strip():
            return "No speech detected."

        return text.strip()

    except Exception as e:

        print(f"Deepgram Error: {e}")

        return "Speech transcription failed."