from speech_to_text import transcribe_audio
from agent import ask_ai

# Speech → Text
user_text = transcribe_audio("recorded_audio.wav")

print("\n🎤 You said:")
print(user_text)

# Text → AI response
prompt = f"""
You are a friendly technical interviewer.

The candidate said:
"{user_text}"

Respond naturally as an interviewer.
If this is a greeting, greet the candidate and then ask
one beginner Python technical interview question.
"""

response = ask_ai(prompt)

print("\n🤖 AI Interviewer:")
print(response)