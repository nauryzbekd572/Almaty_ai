import os
import telebot
from dotenv import load_dotenv
from knowledge_base import KnowledgeBase
from ai_engine import AIEngine

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
db = KnowledgeBase()
ai = AIEngine()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот проекта 'Честное Общество'. Задай мне вопрос о законах РК.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    # 1. Ищем нужную строчку в законах
    relevant_context = db.search_relevant_info(message.text)
    
    # 2. Отправляем эту строчку в ИИ, чтобы он сделал красивый ответ
    ai_response = ai.generate_legal_answer(message.text, relevant_context)
    
    # 3. Отправляем ответ в чат
    bot.reply_to(message, ai_response)

if __name__ == "__main__":
    print("Бот успешно запущен локально...")
    bot.infinity_polling()
