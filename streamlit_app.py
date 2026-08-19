import os
import tempfile

import streamlit as st

from speech_to_text import speech_to_text
from text_to_speech import speak
from ai_interviewer import ask_ai
from interview_report import generate_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Voice Technical Interview",
    page_icon="🎤",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎤 AI Voice Technical Interview")
st.write("Practice a Python / AI Engineer interview using voice.")


# ============================================================
# SETTINGS
# ============================================================

TOTAL_QUESTIONS = 5


# ============================================================
# SESSION STATE
# ============================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "question" not in st.session_state:
    st.session_state.question = "Tell me about yourself."

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "history" not in st.session_state:
    st.session_state.history = []

if "completed" not in st.session_state:
    st.session_state.completed = False

if "report" not in st.session_state:
    st.session_state.report = ""

if "audio_processed" not in st.session_state:
    st.session_state.audio_processed = False


# ============================================================
# START INTERVIEW
# ============================================================

if not st.session_state.started:

    st.info("Click the button below to start your interview.")

    if st.button(
        "🚀 Start Interview",
        use_container_width=True
    ):

        st.session_state.started = True
        st.rerun()


# ============================================================
# INTERVIEW
# ============================================================

elif not st.session_state.completed:

    question_number = st.session_state.question_number
    question = st.session_state.question

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    st.progress(
        question_number / TOTAL_QUESTIONS
    )

    st.subheader(
        f"Question {question_number}/{TOTAL_QUESTIONS}"
    )

    # --------------------------------------------------------
    # AI QUESTION
    # --------------------------------------------------------

    st.markdown(
        f"### 🤖 AI: {question}"
    )

    # --------------------------------------------------------
    # PLAY QUESTION
    # --------------------------------------------------------

    if st.button(
        "🔊 Play Question",
        use_container_width=True
    ):

        try:

            with st.spinner("AI is speaking..."):

                speak(question)

            st.success("Question played successfully!")

        except Exception as e:

            st.warning(
                f"Text-to-Speech is unavailable: {e}"
            )

    # --------------------------------------------------------
    # RECORD ANSWER
    # --------------------------------------------------------

    st.markdown("### 🎙️ Record Your Answer")

    st.write(
        "Click the microphone button below and speak your answer."
    )

    audio = st.audio_input(
        "🎤 Record your answer"
    )

    # --------------------------------------------------------
    # PROCESS AUDIO
    # --------------------------------------------------------

    if audio is not None:

        st.audio(
            audio,
            format="audio/wav"
        )

        if not st.session_state.audio_processed:

            if st.button(
                "✅ Submit Answer",
                use_container_width=True
            ):

                with st.spinner(
                    "🎧 Converting your speech to text..."
                ):

                    try:

                        # Create temporary audio file
                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".wav"
                        ) as temp_audio:

                            temp_audio.write(
                                audio.getvalue()
                            )

                            audio_path = temp_audio.name

                        # Speech-to-text
                        answer = speech_to_text(
                            audio_path
                        )

                        # Delete temporary file
                        try:
                            os.remove(audio_path)
                        except OSError:
                            pass

                        if not answer or not answer.strip():

                            st.error(
                                "❌ Could not understand the audio. "
                                "Please record your answer again."
                            )

                            st.stop()

                        # ------------------------------------------------
                        # DISPLAY ANSWER
                        # ------------------------------------------------

                        st.session_state.audio_processed = True

                        st.success(
                            "✅ Answer recorded successfully!"
                        )

                        st.markdown(
                            "### 📝 Your Answer"
                        )

                        st.write(answer)

                        # ------------------------------------------------
                        # SAVE CONVERSATION
                        # ------------------------------------------------

                        st.session_state.conversation.append(
                            {
                                "question": question,
                                "answer": answer
                            }
                        )

                        st.session_state.history.append(
                            f"Interviewer: {question}\n"
                            f"Candidate: {answer}"
                        )

                        # ------------------------------------------------
                        # NEXT QUESTION
                        # ------------------------------------------------

                        if question_number < TOTAL_QUESTIONS:

                            with st.spinner(
                                "🤖 Generating next interview question..."
                            ):

                                next_question = ask_ai(
                                    "\n\n".join(
                                        st.session_state.history
                                    )
                                )

                            st.session_state.question = (
                                next_question
                            )

                            st.session_state.question_number += 1

                            st.session_state.audio_processed = False

                            st.rerun()

                        # ------------------------------------------------
                        # INTERVIEW COMPLETED
                        # ------------------------------------------------

                        else:

                            st.session_state.completed = True

                            st.rerun()

                    except Exception as e:

                        st.error(
                            f"❌ Speech-to-Text Error: {e}"
                        )

                        st.info(
                            "Please check your Deepgram API key "
                            "and try recording again."
                        )


# ============================================================
# FINAL REPORT
# ============================================================

else:

    st.success(
        "🎉 Interview Completed!"
    )

    st.header(
        "📊 Final Interview Report"
    )

    # --------------------------------------------------------
    # GENERATE REPORT
    # --------------------------------------------------------

    if not st.session_state.report:

        with st.spinner(
            "🤖 Generating your interview feedback..."
        ):

            try:

                st.session_state.report = generate_report(
                    st.session_state.conversation
                )

            except Exception as e:

                st.session_state.report = (
                    f"Unable to generate report.\n\n"
                    f"Error: {e}"
                )

    # --------------------------------------------------------
    # DISPLAY REPORT
    # --------------------------------------------------------

    st.markdown(
        st.session_state.report
    )

    # --------------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------------

    st.download_button(
        label="📥 Download Interview Report",
        data=st.session_state.report,
        file_name="Interview_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

    # --------------------------------------------------------
    # RESTART INTERVIEW
    # --------------------------------------------------------

    st.markdown("---")

    if st.button(
        "🔄 Start New Interview",
        use_container_width=True
    ):

        for key in list(
            st.session_state.keys()
        ):

            del st.session_state[key]

        st.rerun()