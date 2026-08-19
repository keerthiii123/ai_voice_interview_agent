import time

from tts import text_to_speech, save_audio, play_audio
from speech_to_text import record_audio, transcribe_audio
from crew_agents import evaluate_answer


# ============================================================
# INTERVIEW CONFIGURATION
# ============================================================

TOTAL_QUESTIONS = 6

DOMAINS = [
    "Python",
    "Java",
    "Full Stack Development",
    "SQL",
    "General IT",
    "HR and Non-Technical"
]


QUESTIONS = [
    {
        "domain": "Python",
        "question": "What is the difference between a list and a tuple in Python?"
    },
    {
        "domain": "Java",
        "question": "What is the difference between method overloading and method overriding in Java?"
    },
    {
        "domain": "Full Stack Development",
        "question": "What is a REST API and how is it used in a full stack web application?"
    },
    {
        "domain": "SQL",
        "question": "What is the difference between INNER JOIN and LEFT JOIN in SQL?"
    },
    {
        "domain": "General IT",
        "question": "What is the difference between a process and a thread in an operating system?"
    },
    {
        "domain": "HR and Non-Technical",
        "question": "Tell me about yourself and explain why you are interested in this role."
    }
]


# ============================================================
# TTS
# ============================================================

def speak(text):
    """
    Generate speech using Murf TTS.
    """

    if not text:
        return

    audio = text_to_speech(text)

    if audio:
        save_audio(audio, "current_question.wav")

    else:
        print("⚠️ TTS failed.")


# ============================================================
# SPEECH INPUT
# ============================================================

def get_answer():

    print()
    print("🎤 Speak now...")
    print("⏱️ You have 10 seconds...")

    try:
        audio_file = record_audio(duration=10)

    except TypeError:
        # Supports older record_audio() implementations
        audio_file = record_audio()

    except Exception as e:
        print(f"❌ Recording error: {e}")
        return ""

    if not audio_file:
        print("⚠️ No audio recorded.")
        return ""

    try:
        answer = transcribe_audio(audio_file)

    except Exception as e:
        print(f"❌ STT error: {e}")
        return ""

    if not answer:
        print("⚠️ No answer detected.")
        return ""

    return answer.strip()


# ============================================================
# EVALUATION
# ============================================================

def evaluate(question, answer):

    if not answer:
        return {
            "score": 0,
            "strength": "No answer was provided.",
            "weakness": "The question was not answered.",
            "improvement": "Try to answer even if you are unsure."
        }

    try:
        result = evaluate_answer(question, answer)

        return result

    except Exception as e:

        print(f"❌ Evaluation error: {e}")

        return {
            "score": 0,
            "strength": "Unable to evaluate the answer.",
            "weakness": "Evaluation service failed.",
            "improvement": "Please try again."
        }


# ============================================================
# DISPLAY EVALUATION
# ============================================================

def display_evaluation(result):

    print()
    print("📊 Evaluation:")
    print("-" * 50)

    if isinstance(result, dict):

        score = result.get("score", 0)
        strength = result.get("strength", "Not available")
        weakness = result.get("weakness", "Not available")
        improvement = result.get("improvement", "Not available")

        print(f"⭐ Score: {score}/10")

        print()
        print("💪 Strength:")
        print(strength)

        print()
        print("⚠️ Weakness:")
        print(weakness)

        print()
        print("📈 Improvement:")
        print(improvement)

        return score

    else:

        print(result)

        return 0


# ============================================================
# FINAL REPORT
# ============================================================

def generate_final_report(results):

    print()
    print("=" * 60)
    print("📊 FINAL INTERVIEW REPORT")
    print("=" * 60)

    if not results:
        print("⚠️ No interview results available.")
        return

    total_score = sum(item["score"] for item in results)

    average = total_score / len(results)

    print()
    print(f"⭐ Average Score: {average:.1f}/10")

    if average >= 8:
        performance = "Excellent"

    elif average >= 6:
        performance = "Good"

    elif average >= 4:
        performance = "Needs Improvement"

    else:
        performance = "Needs Significant Improvement"

    print(f"🎯 Performance: {performance}")

    print()
    print("-" * 60)
    print("DOMAIN-WISE PERFORMANCE")
    print("-" * 60)

    for item in results:

        print(
            f"{item['domain']:<25} "
            f"{item['score']}/10"
        )

    print()
    print("=" * 60)


# ============================================================
# MAIN INTERVIEW
# ============================================================

def run_interview():

    print("=" * 60)
    print("🤖 AI VOICE MULTI-DOMAIN TECHNICAL INTERVIEW AGENT")
    print("=" * 60)

    print()
    print("🎯 Interview Domains:")

    for index, domain in enumerate(DOMAINS, start=1):
        print(f"{index}. {domain}")

    print()
    print(f"📝 Total Questions: {TOTAL_QUESTIONS}")

    print()
    print("🎤 The AI will ask questions from different domains.")

    print()
    print("🤖 AI Interviewer:")
    print()

    introduction = (
        "Hello! Welcome to your AI voice interview. "
        "This interview contains questions from Python, Java, "
        "Full Stack Development, SQL, General IT, and HR. "
        "Please answer each question clearly. "
        "Let's begin."
    )

    print(introduction)

    speak(introduction)

    time.sleep(1)

    results = []

    # ========================================================
    # QUESTIONS
    # ========================================================

    for index, item in enumerate(QUESTIONS, start=1):

        domain = item["domain"]
        question = item["question"]

        print()
        print("=" * 60)
        print(f"QUESTION {index}/{TOTAL_QUESTIONS}")
        print(f"DOMAIN: {domain}")
        print("=" * 60)

        print()
        print("🤖 AI Interviewer:")
        print(question)

        # Speak question
        speak(question)

        # Record answer
        answer = get_answer()

        print()
        print("🎤 Your Answer:")

        if answer:
            print(answer)

        else:
            print("⚠️ No answer detected.")

        # ====================================================
        # EVALUATION
        # ====================================================

        print()

        if answer:

            print("🧠 Evaluating your answer...")

            result = evaluate(question, answer)

        else:

            result = {
                "score": 0,
                "strength": "No answer was provided.",
                "weakness": "The question was not answered.",
                "improvement": "Try to answer even if you are unsure."
            }

        score = display_evaluation(result)

        results.append(
            {
                "domain": domain,
                "question": question,
                "answer": answer,
                "score": score
            }
        )

        # ====================================================
        # NEXT QUESTION
        # ====================================================

        if index < TOTAL_QUESTIONS:

            next_message = (
                "Thank you for your answer. "
                "Let's move to the next question."
            )

            print()
            print("🤖 AI Interviewer:")
            print(next_message)

            speak(next_message)

            time.sleep(1)

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print()
    print("=" * 60)
    print("📊 INTERVIEW COMPLETED")
    print("=" * 60)

    generate_final_report(results)

    final_message = (
        "Thank you for completing the interview. "
        "Your interview has been completed successfully."
    )

    print()
    print("🤖 AI Interviewer:")
    print(final_message)

    speak(final_message)

    print()
    print("=" * 60)
    print("✅ INTERVIEW COMPLETED SUCCESSFULLY")
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_interview()