from speech_to_text import transcribe_audio

text = transcribe_audio("recorded_audio.wav")

print("\n🎤 You said:")
print(text)