import streamlit as st

audio_value = st.audio_input("🎤 Speak your answer")

if audio_value:
    audio_bytes = audio_value.getvalue()

    with open("answer.wav", "wb") as f:
        f.write(audio_bytes)

    st.success("Audio recorded successfully!")