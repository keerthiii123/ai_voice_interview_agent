import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ============================================================
# GROQ CLIENT
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

MODEL = "openai/gpt-oss-20b"


# ============================================================
# COMMON LLM FUNCTION
# ============================================================

def ask_llm(prompt, temperature=0.3):

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=1200
        )

        content = response.choices[0].message.content

        if not content:
            return "Unable to generate AI response."

        return content.strip()

    except Exception as e:

        print("\n❌ Groq Error:")
        print(e)

        return "Unable to generate AI response."


# ============================================================
# FIRST INTERVIEW QUESTION
# ============================================================

def get_first_question():

    return (
        "Good morning. Can you please introduce yourself "
        "and briefly explain your technical skills and projects?"
    )


# ============================================================
# EVALUATE CANDIDATE ANSWER
# ============================================================

def evaluate_answer(question, answer):

    if not answer or not answer.strip():

        return """Score: 0/10

Strength:
- No answer was provided.

Weakness:
- The candidate did not respond to the question.

Improvement:
- Provide a clear and relevant answer to the question.
"""

    prompt = f"""
You are an experienced technical interviewer.

Evaluate the candidate's answer.

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Return exactly in this format:

Score: X/10

Strength:
- ...

Weakness:
- ...

Improvement:
- ...

Rules:
- Judge only the answer provided.
- Do not invent information.
- Give partial credit when appropriate.
- Focus on technical correctness.
- Consider communication clarity.
- Keep the evaluation concise.
- Be professional and encouraging.
"""

    return ask_llm(prompt, temperature=0.2)


# ============================================================
# GENERATE NEXT INTERVIEW QUESTION
# ============================================================

def generate_next_question(
    previous_question,
    previous_answer,
    domain="Mixed IT"
):

    prompt = f"""
You are a professional Resource Executive conducting a
technical interview.

INTERVIEW DOMAIN:
{domain}

PREVIOUS QUESTION:
{previous_question}

CANDIDATE'S PREVIOUS ANSWER:
{previous_answer}

Ask the next interview question.

Rules:

1. Ask exactly ONE question.
2. Do not provide the answer.
3. Speak naturally like a real Resource Executive.
4. Use the candidate's previous answer to decide the next question.
5. If the answer is strong, slightly increase difficulty.
6. If the answer is weak, ask a simpler follow-up question.
7. Do not repeatedly ask the same question.
8. Questions may cover:

   Python
   Java
   SQL
   HTML
   CSS
   JavaScript
   React
   Django
   REST API
   Git/GitHub
   DBMS
   OOP
   Data Structures
   Machine Learning
   Generative AI
   Cloud basics
   Linux
   Networking
   Software Engineering

9. Do not mention that you are an AI.
10. Return ONLY the question.

Next question:
"""

    return ask_llm(prompt, temperature=0.5)


# ============================================================
# FINAL INTERVIEW FEEDBACK
# ============================================================

def generate_final_feedback(interview_history):

    if not interview_history:

        return """
FINAL INTERVIEW FEEDBACK

Overall Score: 0/10

Technical Knowledge: 0/10

Communication: 0/10

Strengths:
- No interview responses were recorded.

Weaknesses:
- The interview was not completed.

Topics to Practice:
- Complete a full technical interview.

Final Recommendation:
Needs Improvement

Additional Feedback:
Please complete the interview to receive detailed feedback.
"""

    history_text = ""

    for i, item in enumerate(interview_history, start=1):

        # ====================================================
        # DICTIONARY FORMAT
        # ====================================================

        if isinstance(item, dict):

            question = item.get("question", "")
            answer = item.get("answer", "")
            evaluation = item.get("evaluation", "")

        # ====================================================
        # STRING FORMAT
        # ====================================================

        elif isinstance(item, str):

            question = f"Interview Response {i}"
            answer = item
            evaluation = "No separate evaluation was stored."

        # ====================================================
        # OTHER FORMAT
        # ====================================================

        else:

            question = f"Interview Response {i}"
            answer = str(item)
            evaluation = "No separate evaluation was stored."

        history_text += f"""
Question {i}:
{question}

Candidate Answer:
{answer}

Evaluation:
{evaluation}

--------------------------------
"""

    prompt = f"""
You are a senior technical interviewer.

Analyze the complete interview below.

================ INTERVIEW DATA ================

{history_text}

==================================================

Generate a professional final interview feedback report.

Use this exact structure:

FINAL INTERVIEW FEEDBACK

Overall Score: X/10

Technical Knowledge: X/10

Communication: X/10

Strengths:
- ...
- ...
- ...

Weaknesses:
- ...
- ...
- ...

Topics to Practice:
- ...
- ...
- ...

Final Recommendation:
Strong Hire / Hire / Consider / Needs Improvement

Additional Feedback:
...

Rules:

- Base the report ONLY on the provided interview data.
- Do not invent candidate answers.
- Do not assume skills that were not demonstrated.
- Consider technical correctness.
- Consider communication quality.
- Give realistic scores.
- Be honest but encouraging.
- Keep the report professional.
- Do not mention internal AI processing.
"""

    return ask_llm(prompt, temperature=0.2)


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def generate_final_report(interview_history):

    return generate_final_feedback(interview_history)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n==========================================")
    print("AI VOICE INTERVIEW AGENT")
    print("CREW AGENTS TEST")
    print("==========================================")

    question = get_first_question()

    answer = (
        "My name is Keerthana. I have experience in Python, "
        "SQL and Generative AI. I have worked on AI projects "
        "using LangChain and Streamlit."
    )

    print("\nQUESTION:")
    print(question)

    print("\nCANDIDATE ANSWER:")
    print(answer)

    print("\nEVALUATION:")
    print(
        evaluate_answer(
            question,
            answer
        )
    )

    print("\nNEXT QUESTION:")
    print(
        generate_next_question(
            question,
            answer,
            "Mixed IT"
        )
    )