import os

from deepgram import DeepgramClient, PrerecordedOptions


def speech_to_text(audio_file):

    api_key = os.getenv("DEEPGRAM_API_KEY")

    if not api_key:
        raise ValueError(
            "DEEPGRAM_API_KEY is not configured"
        )

    deepgram = DeepgramClient(api_key)

    with open(audio_file, "rb") as audio:
        audio_data = audio.read()

    options = PrerecordedOptions(
        model="nova-2",
        smart_format=True
    )

    response = deepgram.listen.rest.v("1").transcribe_file(
        {
            "buffer": audio_data
        },
        options
    )

    transcript = (
        response
        .results
        .channels[0]
        .alternatives[0]
        .transcript
    )

    return transcript