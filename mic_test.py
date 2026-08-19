import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

sample_rate = 16000
duration = 5
device = 1

print("🎤 Speak now...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16",
    device=device
)

sd.wait()

audio = audio.astype(np.float32)

max_value = np.max(np.abs(audio))

if max_value > 0:
    audio = audio / max_value * 30000

audio = audio.astype(np.int16)

write("recorded_audio.wav", sample_rate, audio)

print("✅ Recording saved!")