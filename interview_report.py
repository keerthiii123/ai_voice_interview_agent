from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_report(conversation):

    # Convert conversation into a clean format
    interview_text = ""

    for i, item in enumerate(conversation, start=1):

        question = item.get("question", "")
        answer = item.get("answer", "")

        interview_text += f"""
QUESTION {i}:
{question}

CANDIDATE ANSWER:
{answer}

"""

    prompt = f"""
You are a strict but fair professional technical interviewer.

The candidate was interviewed for a JUNIOR Python / AI Engineer role.

Evaluate the candidate ONLY using the interview conversation provided below.

============================================================
IMPORTANT EVALUATION RULES
============================================================

1. NEVER invent information.

2. Do NOT assume the candidate has a degree, project,
   job experience, skills, or achievements unless the
   candidate explicitly mentioned them.

3. Do NOT treat the interviewer's questions as candidate
   knowledge.

4. Evaluate ONLY what the candidate actually answered.

5. Speech-to-text may contain small transcription errors.
   Ignore obvious minor transcription mistakes when the
   intended meaning is reasonably clear.

6. If the candidate's answer is unclear or impossible to
   understand, do NOT guess the intended answer.
   Mark the answer as unclear/incomplete.

7. Short answers should NOT automatically receive a low score.
   Score based on relevance and correctness.

8. Completely irrelevant answers should receive a low score.

9. "No speech detected" means the candidate did not provide
   an answer and should receive 0 for that question.

10. Do not give credit for information that appears only in
    the interview questions.

11. Do not give credit for information that appears only in
    the interviewer's instructions.

12. Do not repeat the same strength or weakness.

13. Give EXACTLY 3 strengths.

14. Give EXACTLY 3 weaknesses.

15. Give EXACTLY 3 improvement suggestions.

16. Scores must be integers from 0 to 10.

17. Overall Score should reflect the other scores.

18. Be realistic for a JUNIOR Python / AI Engineer role.

19. Do not automatically recommend rejection.
    The recommendation must match the actual performance.

20. Do not use markdown tables.

============================================================
SCORING GUIDE
============================================================

Technical Knowledge:
0-2 = No meaningful technical knowledge demonstrated
3-4 = Basic awareness but weak understanding
5-6 = Reasonable junior-level knowledge
7-8 = Strong junior-level knowledge
9-10 = Excellent technical knowledge

Communication:
0-2 = Very unclear or mostly irrelevant
3-4 = Difficult to understand
5-6 = Generally understandable
7-8 = Clear and structured
9-10 = Excellent professional communication

Confidence:
0-2 = Very hesitant or unable to answer
3-4 = Low confidence
5-6 = Moderate confidence
7-8 = Good confidence
9-10 = Very confident

Problem Solving:
0-2 = No problem-solving ability demonstrated
3-4 = Limited approach
5-6 = Reasonable approach
7-8 = Strong structured approach
9-10 = Excellent analytical approach

============================================================
OUTPUT FORMAT
============================================================

Return EXACTLY this format:

============================================================
FINAL INTERVIEW FEEDBACK
============================================================

Overall Score: X/10
Technical Knowledge: X/10
Communication: X/10
Confidence: X/10
Problem Solving: X/10

------------------------------------------------------------
STRENGTHS
------------------------------------------------------------

- ...
- ...
- ...

------------------------------------------------------------
WEAKNESSES
------------------------------------------------------------

- ...
- ...
- ...

------------------------------------------------------------
AREAS FOR IMPROVEMENT
------------------------------------------------------------

- ...
- ...
- ...

------------------------------------------------------------
FINAL RECOMMENDATION
------------------------------------------------------------

...

------------------------------------------------------------
INTERVIEW SUMMARY
------------------------------------------------------------

...

============================================================

INTERVIEW CONVERSATION:

{interview_text}
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
            temperature=0.1,
            max_tokens=900
        )

        report = response.choices[0].message.content.strip()

        return report

    except Exception as e:

        return f"""
============================================================
FINAL INTERVIEW FEEDBACK
============================================================

Report generation failed.

Error:
{e}

============================================================
"""