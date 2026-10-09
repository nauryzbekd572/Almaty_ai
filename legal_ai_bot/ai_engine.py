import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-2.5-flash"

    def generate_legal_answer(self, user_question: str, context: str) -> str:
        system_instruction = (
            "Вы — AI-ассистент проекта 'Честное общество'. "
            "Отвечайте строго на основе предоставленного Контекста. Если ответа нет, скажите, что не знаете."
        )
        prompt = f"Контекст:\n{context}\n\nВопрос: {user_question}"
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                )
            )
            return response.text
        except Exception as e:
            return f"Ошибка ИИ: {str(e)}"
