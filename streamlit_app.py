import streamlit as st

from speech_to_text import transcribe_audio
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

st.write(
    "Practice a Python / AI Engineer interview using voice."
)


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

if "current_audio_id" not in st.session_state:
    st.session_state.current_audio_id = None

if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False


# ============================================================
# START INTERVIEW
# ============================================================

if not st.session_state.started:

    st.info(
        "Click the button below to start your AI technical interview."
    )

    st.markdown("""
    ### Interview Process

    1. 🤖 AI asks a technical question
    2. 🎙️ You answer using your microphone
    3. 📝 Deepgram converts your speech to text
    4. 🧠 AI generates the next question
    5. 📊 Final AI-powered interview report
    """)

    if st.button(
        "🚀 Start Interview",
        use_container_width=True
    ):

        st.session_state.started = True
        st.session_state.question_number = 1
        st.session_state.question = "Tell me about yourself."
        st.session_state.conversation = []
        st.session_state.history = []
        st.session_state.completed = False
        st.session_state.report = ""
        st.session_state.current_audio_id = None
        st.session_state.answer_submitted = False

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

    st.markdown("### 🔊 Interviewer")

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

    st.markdown("---")

    st.markdown("### 🎙️ Record Your Answer")

    st.write(
        "Click the microphone button and speak your answer."
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


        # Create unique ID for current recording

        audio_id = hash(audio.getvalue())


        # Reset submit state for a new recording

        if st.session_state.current_audio_id != audio_id:

            st.session_state.current_audio_id = audio_id
            st.session_state.answer_submitted = False


        # ----------------------------------------------------
        # SUBMIT ANSWER
        # ----------------------------------------------------

        if not st.session_state.answer_submitted:

            if st.button(
                "✅ Submit Answer",
                use_container_width=True
            ):

                with st.spinner(
                    "🎧 Converting your speech to text..."
                ):

                    try:

                        # Send browser audio directly
                        # to Deepgram

                        answer = transcribe_audio(
                            audio.getvalue()
                        )


                        # ------------------------------------------------
                        # CHECK RESULT
                        # ------------------------------------------------

                        if not answer:

                            st.error(
                                "No answer detected. "
                                "Please record your answer again."
                            )

                            st.stop()


                        if answer.startswith(
                            "Speech-to-Text Error:"
                        ):

                            st.error(answer)

                            st.warning(
                                "Please record your answer again."
                            )

                            st.stop()


                        if answer == "No speech detected.":

                            st.warning(
                                "No speech detected. "
                                "Please speak clearly and try again."
                            )

                            st.stop()


                        # ------------------------------------------------
                        # DISPLAY ANSWER
                        # ------------------------------------------------

                        st.success(
                            "Answer recorded successfully!"
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


                        st.session_state.answer_submitted = True


                        # ------------------------------------------------
                        # NEXT QUESTION
                        # ------------------------------------------------

                        if question_number < TOTAL_QUESTIONS:

                            with st.spinner(
                                "🧠 Generating next interview question..."
                            ):

                                try:

                                    next_question = ask_ai(
                                        "\n\n".join(
                                            st.session_state.history
                                        )
                                    )

                                except Exception as e:

                                    st.error(
                                        f"AI question generation failed: {e}"
                                    )

                                    st.stop()


                            if not next_question:

                                st.error(
                                    "Unable to generate the next question."
                                )

                                st.stop()


                            st.session_state.question = (
                                next_question
                            )

                            st.session_state.question_number += 1

                            st.session_state.current_audio_id = None

                            st.session_state.answer_submitted = False

                            st.rerun()


                        # ------------------------------------------------
                        # INTERVIEW COMPLETED
                        # ------------------------------------------------

                        else:

                            st.session_state.completed = True

                            st.rerun()


                    except Exception as e:

                        st.error(
                            f"Speech-to-Text Error: {e}"
                        )

                        st.info(
                            "Please check your microphone and "
                            "Deepgram API configuration."
                        )


# ============================================================
# FINAL REPORT
# ============================================================

else:

    st.success("🎉 Interview Completed!")

    st.header("📊 Final Interview Report")


    # --------------------------------------------------------
    # GENERATE REPORT
    # --------------------------------------------------------

    if not st.session_state.report:

        with st.spinner(
            "🧠 Generating your interview feedback..."
        ):

            try:

                st.session_state.report = generate_report(
                    st.session_state.conversation
                )

            except Exception as e:

                st.session_state.report = (
                    "Report generation failed.\n\n"
                    f"Error: {e}"
                )


    # --------------------------------------------------------
    # DISPLAY REPORT
    # --------------------------------------------------------

    st.markdown(
        st.session_state.report
    )


    # --------------------------------------------------------
    # INTERVIEW DETAILS
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("📋 Interview Details")

    st.write(
        f"**Total Questions:** {TOTAL_QUESTIONS}"
    )

    st.write(
        f"**Questions Answered:** "
        f"{len(st.session_state.conversation)}"
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
    # SHOW CONVERSATION
    # --------------------------------------------------------

    with st.expander("💬 View Interview Conversation"):

        for index, item in enumerate(
            st.session_state.conversation,
            start=1
        ):

            st.markdown(
                f"### Question {index}"
            )

            st.write(
                f"**🤖 AI:** {item['question']}"
            )

            st.write(
                f"**🎙️ Candidate:** {item['answer']}"
            )

            st.markdown("---")


    # --------------------------------------------------------
    # RESTART
    # --------------------------------------------------------

    if st.button(
        "🔄 Start New Interview",
        use_container_width=True
    ):

        for key in list(
            st.session_state.keys()
        ):

            del st.session_state[key]

        st.rerun()