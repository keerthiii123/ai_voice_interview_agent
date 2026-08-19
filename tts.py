import os
import uuid
import asyncio

from edge_tts import Communicate
from playsound import playsound


# ============================================================
# TEXT TO SPEECH
# ============================================================

def text_to_speech(text):
    """
    Convert text into speech and play it.
    """

    if not text or not text.strip():
        return

    filename = f"tts_{uuid.uuid4().hex}.mp3"

    async def generate_audio():
        communicate = Communicate(
            text=text,
            voice="en-US-AriaNeural"
        )

        await communicate.save(filename)

    try:

        # Generate speech
        asyncio.run(generate_audio())

        # Play speech
        playsound(filename)

    except Exception as e:

        print("\n❌ TTS Error:")
        print(e)

    finally:

        # Delete temporary audio file
        if os.path.exists(filename):

            try:
                os.remove(filename)

            except Exception:
                pass