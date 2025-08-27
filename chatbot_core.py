# chatbot_core.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

class Chatbot:
    def __init__(self):
        pass

    def _chat(self, prompt: str) -> str:
        """Call LLM via Groq to generate questions."""
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are TalentScout's friendly technical interviewer."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("Groq API error:", e)
            return "Oops! Something went wrong generating questions."

    def generate_tech_questions(self, candidate_data):
        """Generate 15 questions evenly across tech stack using LLM."""
        tech_stack = candidate_data.data.get("tech_stack", [])
        if not tech_stack:
            return ["No tech stack provided. Please list your skills."]

        total_questions = 15
        per_tech = total_questions // len(tech_stack)
        extra = total_questions % len(tech_stack)

        all_questions = []
        for i, tech in enumerate(tech_stack):
            q_count = per_tech + (1 if i < extra else 0)
            prompt = (
                f"Create {q_count} clear, concise interview questions "
                f"for the skill '{tech}'. List each question on a new line."
            )
            questions_text = self._chat(prompt)
            questions_list = [q.strip() for q in questions_text.splitlines() if q.strip()]
            all_questions.extend(questions_list)
        return all_questions
