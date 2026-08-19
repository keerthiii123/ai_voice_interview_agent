import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(question):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI technical interviewer. "
                    "Ask clear technical questions and evaluate "
                    "the candidate's answers."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content