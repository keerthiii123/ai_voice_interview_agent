import streamlit as st
from speech_to_text import speech_to_text
from text_to_speech import speak
from ai_interviewer import ask_ai
from interview_report import generate_report


st.set_page_config(
    page_title="AI Voice Technical Interview",
    page_icon="🎤",
    layout="centered"
)


st.title("🎤 AI Voice Technical Interview")
st.write("Practice a Python / AI Engineer interview using voice.")


TOTAL_QUESTIONS = 5


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# START INTERVIEW
# ------------------------------------------------------------

if not st.session_state.started:

    st.info("Click the button below to start your interview.")

    if st.button("🚀 Start Interview", use_container_width=True):

        st.session_state.started = True

        st.rerun()


# ------------------------------------------------------------
# INTERVIEW
# ------------------------------------------------------------

elif not st.session_state.completed:

    question_number = st.session_state.question_number
    question = st.session_state.question

    st.progress(
        question_number / TOTAL_QUESTIONS
    )

    st.subheader(
        f"Question {question_number}/{TOTAL_QUESTIONS}"
    )

    st.markdown(
        f"### 🤖 AI: {question}"
    )


    # --------------------------------------------------------
    # AI SPEAK
    # --------------------------------------------------------

    if st.button(
        "🔊 Play Question",
        use_container_width=True
    ):

        speak(question)


    # --------------------------------------------------------
    # RECORD ANSWER
    # --------------------------------------------------------

    if st.button(
        "🎙️ Record My Answer",
        use_container_width=True
    ):

        with st.spinner("Listening to your answer..."):

            answer = speech_to_text()


        st.success("Answer recorded!")

        st.markdown("### 📝 Your Answer")

        st.write(answer)


        # Save conversation

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


        # ----------------------------------------------------
        # NEXT QUESTION
        # ----------------------------------------------------

        if question_number < TOTAL_QUESTIONS:

            with st.spinner("Generating next question..."):

                next_question = ask_ai(
                    "\n\n".join(
                        st.session_state.history
                    )
                )

            st.session_state.question = next_question

            st.session_state.question_number += 1

            st.rerun()

        else:

            st.session_state.completed = True

            st.rerun()


# ------------------------------------------------------------
# FINAL REPORT
# ------------------------------------------------------------

else:

    st.success("🎉 Interview Completed!")

    st.header("📊 Final Interview Report")


    if not st.session_state.report:

        with st.spinner("Generating your interview feedback..."):

            st.session_state.report = generate_report(
                st.session_state.conversation
            )


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
    # RESTART
    # --------------------------------------------------------

    if st.button(
        "🔄 Start New Interview",
        use_container_width=True
    ):

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        st.rerun()