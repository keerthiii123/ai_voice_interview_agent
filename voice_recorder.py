import sounddevice as sd
import numpy as np
import webrtcvad
import wave

SAMPLE_RATE = 16000
CHANNELS = 1
FRAME_DURATION = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION / 1000)

vad = webrtcvad.Vad(2)


def record_until_silence(filename="user_answer.wav"):
    print("\n🎤 Speak now...")

    frames = []
    silence_count = 0
    started = False

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        device=1,
        blocksize=FRAME_SIZE
    )

    with stream:
        while True:
            audio, _ = stream.read(FRAME_SIZE)

            audio_bytes = audio.tobytes()

            is_speech = vad.is_speech(
                audio_bytes,
                SAMPLE_RATE
            )

            if is_speech:
                started = True
                silence_count = 0
                frames.append(audio_bytes)

            elif started:
                frames.append(audio_bytes)
                silence_count += 1

                # ~1.5 seconds silence
                if silence_count >= 50:
                    break

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(frames))

    print("✅ Recording stopped.")

    return filename