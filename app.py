from speech_to_text import speech_to_text
from text_to_speech import speak
from ai_interviewer import ask_ai
from interview_report import generate_report


# ============================================================
# AI VOICE TECHNICAL INTERVIEW
# ============================================================

print("\n" + "=" * 60)
print("        AI VOICE TECHNICAL INTERVIEW")
print("=" * 60)

TOTAL_QUESTIONS = 5

question = "Tell me about yourself."

conversation = []
history = []

# Maximum retries for invalid answers
MAX_RETRIES = 2


# ============================================================
# ANSWER VALIDATION
# ============================================================

def is_valid_answer(answer):

    if not answer:
        return False

    answer = answer.strip()

    if not answer:
        return False

    # Deepgram did not detect speech
    if answer.lower() == "no speech detected.":
        return False

    # Very short answers
    if len(answer.split()) < 3:
        return False

    # Reject answers containing only numbers
    cleaned = answer.replace(".", "").replace(",", "").replace(" ", "")

    if cleaned.isdigit():
        return False

    # Reject common accidental responses
    invalid_answers = [
        "hello",
        "hi",
        "bye",
        "bye bye",
        "thank you",
        "thanks"
    ]

    if answer.lower() in invalid_answers:
        return False

    return True


# ============================================================
# INTERVIEW LOOP
# ============================================================

question_number = 1

while question_number <= TOTAL_QUESTIONS:

    print("\n" + "=" * 60)
    print(f"QUESTION {question_number}/{TOTAL_QUESTIONS}")
    print("=" * 60)

    print(f"\nAI: {question}")

    # --------------------------------------------------------
    # AI SPEAKS
    # --------------------------------------------------------

    speak(question)

    # --------------------------------------------------------
    # ANSWER RETRY LOOP
    # --------------------------------------------------------

    retry_count = 0
    answer = ""

    while retry_count <= MAX_RETRIES:

        print("\nListening for your answer...")

        answer = speech_to_text()

        print(f"\nCandidate: {answer}")

        # Valid answer
        if is_valid_answer(answer):
            break

        retry_count += 1

        if retry_count <= MAX_RETRIES:

            print("\n" + "-" * 60)
            print("I couldn't understand your answer.")
            print("Please answer the question again.")
            print("-" * 60)

            speak(
                "I couldn't understand your answer. "
                "Please answer the question again."
            )

    # --------------------------------------------------------
    # IF STILL INVALID AFTER RETRIES
    # --------------------------------------------------------

    if not is_valid_answer(answer):

        print("\nNo valid answer received.")

        # Store it for report, but continue interview
        answer = "No valid answer provided."

    # --------------------------------------------------------
    # SAVE CONVERSATION
    # --------------------------------------------------------

    conversation.append({
        "question": question,
        "answer": answer
    })

    history.append(
        f"Interviewer: {question}\n"
        f"Candidate: {answer}"
    )

    # --------------------------------------------------------
    # GET NEXT QUESTION
    # --------------------------------------------------------

    if question_number < TOTAL_QUESTIONS:

        print("\nGenerating next interview question...")

        question = ask_ai("\n\n".join(history))

    question_number += 1


# ============================================================
# INTERVIEW COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("        INTERVIEW COMPLETED")
print("=" * 60)


# ============================================================
# GENERATE REPORT
# ============================================================

print("\nGenerating report...")

report = generate_report(conversation)


# ============================================================
# DISPLAY REPORT
# ============================================================

print("\n")
print(report)


# ============================================================
# SAVE REPORT
# ============================================================

REPORT_FILE = "Interview_Report.txt"

with open(REPORT_FILE, "w", encoding="utf-8") as file:
    file.write(report)

print("\n" + "=" * 60)
print(f"Report saved: {REPORT_FILE}")
print("=" * 60)