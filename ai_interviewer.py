from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(history):

    prompt = f"""
You are a professional AI Technical Interviewer.

You are interviewing a candidate for a Python / AI Engineer role.

Previous interview conversation:

{history}

Your task is to ask the NEXT interview question.

IMPORTANT RULES:

- Return ONLY ONE question.
- Do NOT provide explanations.
- Do NOT provide reasoning.
- Do NOT provide <think> tags.
- Do NOT provide a numbered list.
- Do NOT ask multiple questions.
- Keep the question clear and conversational.
- The question must be suitable for a junior/intermediate Python AI Engineer.
- Avoid extremely advanced topics such as custom transformer training, distributed training, CUDA optimization, or advanced mathematical theory.
- Do not repeat a previous question.

Use this interview progression:

Question 1:
Candidate introduction and background.

Question 2:
Python and AI technical skills.

Question 3:
AI/Python project experience.

Question 4:
Problem solving or Python coding concepts.

Question 5:
Career motivation and AI Engineer role.

Based on the conversation, ask the most appropriate NEXT question.

Return ONLY the question.

"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=150
        )

        question = response.choices[0].message.content.strip()

        # Remove accidental reasoning tags
        if "<think>" in question:
            question = question.split("</think>")[-1].strip()

        # Remove common prefixes
        prefixes = [
            "Question:",
            "Next question:",
            "Interviewer:"
        ]

        for prefix in prefixes:
            if question.startswith(prefix):
                question = question[len(prefix):].strip()

        return question

    except Exception as e:

        print(f"Groq Error: {e}")

        return "Can you describe your experience with Python?"