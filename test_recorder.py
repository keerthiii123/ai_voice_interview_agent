from voice_recorder import record_until_silence

file = record_until_silence()

print("Saved:", file)