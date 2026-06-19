from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


# =========================
# GENERATE QUESTIONS
# =========================
def generate_questions(role: str, difficulty: str, num_questions: int) -> list[str]:
    prompt = f"""
Generate {num_questions} interview questions for a {role} position.
Difficulty: {difficulty}

Return only questions.
One question per line.
No numbering.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    questions = response.text.split("\n")

    return [q.strip() for q in questions if q.strip()]


# =========================
# EVALUATE ANSWER (FIXED)
# =========================
import json
import re

def evaluate_answer(question: str, answer: str):

    prompt = f"""
You are an expert interviewer.

Return ONLY valid JSON:

{{
  "score": 0-100,
  "feedback": "short feedback"
}}

Question: {question}
Answer: {answer}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    print("RAW GEMINI RESPONSE:", text)

    try:
        # 🔥 extract JSON safely from messy output
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            return {
                "score": 0,
                "feedback": "AI returned invalid format"
            }

        data = json.loads(match.group())

        return {
            "score": int(data.get("score", 0)),
            "feedback": data.get("feedback", "No feedback")
        }

    except Exception as e:
        print("PARSE ERROR:", e)

        return {
            "score": 0,
            "feedback": "Evaluation failed due to parsing error"
        }


# =========================
# SUMMARY (KEEP GEMINI)
# =========================
def generate_ai_summary(
    role: str,
    difficulty: str,
    total_questions: int,
    answered_questions: int,
    average_score: float,
    feedback_text: str
):
    prompt = f"""
You are an expert interviewer.

Role: {role}
Difficulty: {difficulty}
Total Questions: {total_questions}
Answered: {answered_questions}
Average Score: {average_score}

Feedbacks:
{feedback_text}

Give:
1. Summary
2. Strengths
3. Improvements

Keep under 150 words.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

    print("LOADED KEY:", GEMINI_API_KEY[:10])  # prints first 10 chars