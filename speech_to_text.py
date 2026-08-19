import os
from deepgram import DeepgramClient, PrerecordedOptions


def speech_to_text(audio_file):
    api_key = os.getenv("DEEPGRAM_API_KEY")

    deepgram = DeepgramClient(api_key)

    with open(audio_file, "rb") as audio:
        buffer_data = audio.read()

    options = PrerecordedOptions(
        model="nova-2",
        smart_format=True
    )

    response = deepgram.listen.rest.v("1").transcribe_file(
        {"buffer": buffer_data},
        options
    )

    return response.results.channels[0].alternatives[0].transcript