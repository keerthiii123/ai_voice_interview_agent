import streamlit as st

from speech_to_text import transcribe_audio
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
# SESSION STATE INITIALIZATION
# ============================================================

default_state = {
    "started": False,
    "question_number": 1,
    "question": "Tell me about yourself.",
    "conversation": [],
    "history": [],
    "completed": False,
    "report": "",
    "last_audio_id": None,
    "answer_submitted": False,
}

for key, value in default_state.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# START INTERVIEW
# ============================================================

if not st.session_state.started:

    st.info(
        "Click the button below to start your Python / AI Engineer interview."
    )

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
        st.session_state.last_audio_id = None
        st.session_state.answer_submitted = False

        st.rerun()


# ============================================================
# INTERVIEW SECTION
# ============================================================

elif not st.session_state.completed:

    question_number = st.session_state.question_number
    question = st.session_state.question

    # ========================================================
    # PROGRESS
    # ========================================================

    st.progress(
        question_number / TOTAL_QUESTIONS
    )

    st.subheader(
        f"Question {question_number}/{TOTAL_QUESTIONS}"
    )

    # ========================================================
    # AI QUESTION
    # ========================================================

    st.markdown(
        f"### 🤖 AI: {question}"
    )

    # ========================================================
    # INTERVIEWER
    # ========================================================

    st.markdown("### 🔊 Interviewer")

    st.info(
        "Please read the question above and answer using the microphone."
    )

    # ========================================================
    # RECORD ANSWER
    # ========================================================

    st.markdown("### 🎙️ Record Your Answer")

    st.write(
        "Click the microphone button and speak your answer."
    )

    audio = st.audio_input(
        "🎤 Record your answer"
    )

    # ========================================================
    # AUDIO AVAILABLE
    # ========================================================

    if audio is not None:

        st.audio(
            audio,
            format="audio/wav"
        )

        # ----------------------------------------------------
        # CREATE UNIQUE AUDIO ID
        # ----------------------------------------------------

        audio_bytes = audio.getvalue()

        audio_id = hash(audio_bytes)

        # ----------------------------------------------------
        # RESET SUBMISSION STATE FOR NEW RECORDING
        # ----------------------------------------------------

        if st.session_state.last_audio_id != audio_id:

            st.session_state.answer_submitted = False

            st.session_state.last_audio_id = audio_id

        # ----------------------------------------------------
        # SUBMIT ANSWER
        # ----------------------------------------------------

        if not st.session_state.answer_submitted:

            if st.button(
                "✅ Submit Answer",
                use_container_width=True
            ):

                st.session_state.answer_submitted = True

                # ====================================================
                # SPEECH TO TEXT
                # ====================================================

                with st.spinner(
                    "🎧 Converting your speech to text..."
                ):

                    try:

                        answer = transcribe_audio(
                            audio_bytes
                        )

                    except Exception as e:

                        st.session_state.answer_submitted = False

                        st.error(
                            f"Speech-to-Text Error: {e}"
                        )

                        st.info(
                            "Please check your DEEPGRAM_API_KEY "
                            "in Streamlit Secrets."
                        )

                        st.stop()

                # ====================================================
                # VALIDATE ANSWER
                # ====================================================

                if (
                    not answer
                    or not answer.strip()
                    or answer.lower().startswith(
                        "speech-to-text error"
                    )
                ):

                    st.session_state.answer_submitted = False

                    st.error(
                        "Could not understand your answer. "
                        "Please record again."
                    )

                    st.stop()

                # ====================================================
                # DISPLAY ANSWER
                # ====================================================

                st.success(
                    "Answer recorded successfully!"
                )

                st.markdown(
                    "### 📝 Your Answer"
                )

                st.write(answer)

                # ====================================================
                # SAVE CONVERSATION
                # ====================================================

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

                # ====================================================
                # GENERATE NEXT QUESTION
                # ====================================================

                if question_number < TOTAL_QUESTIONS:

                    with st.spinner(
                        "🤖 Generating next interview question..."
                    ):

                        try:

                            history_text = "\n\n".join(
                                st.session_state.history
                            )

                            next_question = ask_ai(
                                history_text
                            )

                        except Exception as e:

                            st.error(
                                f"Unable to generate the next question: {e}"
                            )

                            st.stop()

                    # ------------------------------------------------
                    # VALIDATE NEXT QUESTION
                    # ------------------------------------------------

                    if (
                        not next_question
                        or not next_question.strip()
                    ):

                        st.error(
                            "Unable to generate the next question."
                        )

                        st.stop()

                    # ------------------------------------------------
                    # SAVE NEXT QUESTION
                    # ------------------------------------------------

                    st.session_state.question = (
                        next_question.strip()
                    )

                    st.session_state.question_number += 1

                    st.session_state.last_audio_id = None

                    st.session_state.answer_submitted = False

                    st.rerun()

                # ====================================================
                # INTERVIEW COMPLETED
                # ====================================================

                else:

                    st.session_state.completed = True

                    st.rerun()


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

    # ========================================================
    # GENERATE REPORT
    # ========================================================

    if not st.session_state.report:

        with st.spinner(
            "📊 Generating your interview feedback..."
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

    # ========================================================
    # DISPLAY REPORT
    # ========================================================

    st.markdown(
        st.session_state.report
    )

    # ========================================================
    # INTERVIEW DETAILS
    # ========================================================

    st.markdown(
        "### 📋 Interview Details"
    )

    st.write(
        f"**Total Questions:** {TOTAL_QUESTIONS}"
    )

    st.write(
        f"**Questions Answered:** "
        f"{len(st.session_state.conversation)}"
    )

    # ========================================================
    # VIEW CONVERSATION
    # ========================================================

    with st.expander(
        "💬 View Interview Conversation"
    ):

        for index, item in enumerate(
            st.session_state.conversation,
            start=1
        ):

            st.markdown(
                f"**Question {index}:**"
            )

            st.write(
                item["question"]
            )

            st.markdown(
                "**Candidate:**"
            )

            st.write(
                item["answer"]
            )

            st.divider()

    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    st.download_button(
        label="📥 Download Interview Report",
        data=st.session_state.report,
        file_name="Interview_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

    # ========================================================
    # DOWNLOAD CONVERSATION
    # ========================================================

    conversation_text = ""

    for index, item in enumerate(
        st.session_state.conversation,
        start=1
    ):

        conversation_text += (
            f"\nQUESTION {index}\n"
            f"{item['question']}\n\n"
            f"CANDIDATE ANSWER\n"
            f"{item['answer']}\n"
            f"\n{'=' * 60}\n"
        )

    st.download_button(
        label="📄 Download Interview Conversation",
        data=conversation_text,
        file_name="Interview_Conversation.txt",
        mime="text/plain",
        use_container_width=True
    )

    # ========================================================
    # RESTART INTERVIEW
    # ========================================================

    if st.button(
        "🔄 Start New Interview",
        use_container_width=True
    ):

        for key in list(
            st.session_state.keys()
        ):

            del st.session_state[key]

        st.rerun()