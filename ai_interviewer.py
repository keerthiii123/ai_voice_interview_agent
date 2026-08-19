import os

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ============================================================
# GROQ CLIENT
# ============================================================

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured in the .env file."
    )

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# FALLBACK QUESTIONS
# ============================================================

FALLBACK_QUESTIONS = [
    "Can you tell me about your experience with Python for AI, including the libraries or frameworks you have worked with?",

    "Can you describe a recent AI project you built using Python and explain the problem it solved?",

    "How would you handle missing values in a pandas DataFrame?",

    "What motivates you to pursue a career as an AI Engineer?"
]


# ============================================================
# ASK NEXT INTERVIEW QUESTION
# ============================================================

def ask_ai(history):

    prompt = f"""
You are a professional AI Technical Interviewer.

You are interviewing a candidate for a Junior/Intermediate
Python and AI Engineer role.

Previous interview conversation:

{history}

Your task is to ask the NEXT appropriate interview question.

INTERVIEW PROGRESSION:

1. Candidate introduction and background
2. Python and AI technical skills
3. AI/Python project experience
4. Python problem solving or coding concepts
5. Career motivation and AI Engineer role

IMPORTANT RULES:

- Return ONLY ONE question.
- Return plain text only.
- Do NOT provide an answer.
- Do NOT provide an explanation.
- Do NOT provide reasoning.
- Do NOT use <think> tags.
- Do NOT use markdown.
- Do NOT use a numbered list.
- Do NOT ask multiple questions.
- Do NOT repeat a previous question.
- Keep the question conversational.
- Keep it suitable for a junior/intermediate candidate.
- Avoid extremely advanced topics.
- Focus on Python, AI, machine learning, projects,
  problem solving, or career motivation.

Based on the previous conversation, generate the next
appropriate interview question.

Return ONLY the question.
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional technical "
                        "interviewer. Return only one question."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=120
        )


        # ----------------------------------------------------
        # GET RESPONSE
        # ----------------------------------------------------

        question = response.choices[0].message.content


        # ----------------------------------------------------
        # VALIDATE RESPONSE
        # ----------------------------------------------------

        if question is None:

            print("Groq returned empty response.")

            return get_fallback_question(history)


        question = question.strip()


        if not question:

            print("Groq returned blank question.")

            return get_fallback_question(history)


        # ----------------------------------------------------
        # REMOVE THINK TAGS
        # ----------------------------------------------------

        if "<think>" in question:

            if "</think>" in question:

                question = question.split(
                    "</think>"
                )[-1].strip()

            else:

                question = question.split(
                    "<think>"
                )[0].strip()


        # ----------------------------------------------------
        # REMOVE COMMON PREFIXES
        # ----------------------------------------------------

        prefixes = [
            "Question:",
            "Next question:",
            "Interviewer:",
            "Q:"
        ]

        for prefix in prefixes:

            if question.lower().startswith(
                prefix.lower()
            ):

                question = question[
                    len(prefix):
                ].strip()


        # ----------------------------------------------------
        # REMOVE QUOTES
        # ----------------------------------------------------

        question = question.strip('"').strip("'").strip()


        # ----------------------------------------------------
        # FINAL VALIDATION
        # ----------------------------------------------------

        if not question:

            return get_fallback_question(history)


        if len(question) < 10:

            print(
                "Groq generated an invalid question:",
                question
            )

            return get_fallback_question(history)


        # ----------------------------------------------------
        # ENSURE QUESTION MARK
        # ----------------------------------------------------

        if not question.endswith("?"):

            question += "?"


        print(
            "\nGenerated next question:",
            question
        )


        return question


    except Exception as e:

        print(
            "\nGroq Error:",
            str(e)
        )

        return get_fallback_question(history)


# ============================================================
# FALLBACK QUESTION FUNCTION
# ============================================================

def get_fallback_question(history):

    history_lower = history.lower()


    # Question 2
    if (
        "tell me about yourself" in history_lower
        and "python" not in history_lower
    ):

        return (
            "Can you tell me about your experience "
            "with Python for AI, including the libraries "
            "or frameworks you have worked with?"
        )


    # Question 3
    if (
        "python" in history_lower
        and "project" not in history_lower
    ):

        return (
            "Can you describe a recent AI project you "
            "built using Python and explain the problem "
            "it solved?"
        )


    # Question 4
    if (
        "project" in history_lower
    ):

        return (
            "How would you handle missing values "
            "in a pandas DataFrame?"
        )


    # Question 5
    return (
        "What motivates you to pursue a career "
        "as an AI Engineer?"
    )