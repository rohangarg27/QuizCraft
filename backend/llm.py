import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # ✅ correct way
model = genai.GenerativeModel("gemini-1.5-flash")     # ✅ free tier

def generate_quiz(context: str, topic: str, num_questions: int = 5) -> str:
    prompt = f"""
    Create {num_questions} multiple-choice questions (with 4 options each + correct answer)
    based on this NCERT context about {topic}:

    {context}
    """
    response = model.generate_content(prompt)   # ✅ use flash model
    return response.text
