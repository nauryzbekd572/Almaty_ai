import os
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from database.base import AsyncSessionLocal
from database.models import User, Complaint
from services.ai_service import AIService
from services.doc_service import DocGenerator

router = Router()
ai_service = AIService()

# Состояния FSM согласно правилам проектирования aiogram 3.x
class ComplaintSteps(StatesGroup):
    waiting_for_name = State()
    waiting_for_issue = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Главное меню с идеологическим уклоном регламента (п. 4.1)
    kb = [
        [types.KeyboardButton(text="⚖️ Юридическая консультация (Конституция 2026)")],
        [types.KeyboardButton(text="📝 Подать официальное обращение")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        f"Саламатсыз ба, {message.from_user.first_name}! 👋\n"
        f"Вас приветствует интеллектуальный консультант проекта **«Адал қоғам»**.\n\n"
        f"Я функционирую на базе ценностей правовой грамотности, концепций «Закон и Порядок», "
        f"«Адал азамат» и «Таза Қазақстан». Помогу вам проанализировать проблему и составить "
        f"официальное заявление на основе Новой Конституции 2026 года.",
        reply_markup=keyboard
    )

@router.message(F.text == "📝 Подать официальное обращение")
async def start_complaint_flow(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваше **ФИО** для автоматического формирования юридического бланка:")
    await state.set_state(ComplaintSteps.waiting_for_name)

@router.message(ComplaintSteps.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(
        "Опишите вашу проблему или факт правонарушения во всех подробностях.\n\n"
        "Например: *«Во дворе дома по улице Абая обнаружена несанкционированная свалка строительного мусора...»* "
        "или *«Столкнулся с проявлением бюрократии и нарушением моих прав в государственном учреждении...»*"
    )
    await state.set_state(ComplaintSteps.waiting_for_issue)

@router.message(ComplaintSteps.waiting_for_issue)
async def process_issue(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    full_name = user_data.get("full_name")
    raw_text = message.text
    telegram_id = message.from_user.id

    # Отправляем визуальный статус "печать", чтобы пользователь видел, что бот думает
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    status_msg = await message.answer("⏳ *ИИ-юрист анализирует обращение на соответствие нормам Конституции 2026 года...*")

    # 1. Запрос к AI сервису
    ai_result = await ai_service.analyze_incident(raw_text)
    category = ai_result.get("category", "Закон и Порядок")
    resolution = ai_result.get("resolution", "Правовое заключение формируется.")

    # 2. Асинхронная работа с Базой Данных (Выполнение требований п. 2 и п. 9.2)
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Проверяем, существует ли пользователь в базе
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            db_user = result.scalar_one_or_none()

            if not db_user:
                db_user = User(telegram_id=telegram_id, full_name=full_name)
                session.add(db_user)

            # Сохраняем обращение и вердикт ИИ
            complaint = Complaint(
                user_id=telegram_id,
                issue_type=category,
                raw_text=raw_text,
                ai_resolution=resolution
            )
            session.add(complaint)
            await session.commit()

    # 3. Генерация Word-документа (.docx) по стандартам Times New Roman (п. 1.2, 4.1)
    doc_filename = f"Заявление_{telegram_id}.docx"
    DocGenerator.generate_complaint_docx(
        user_name=full_name,
        issue_type=category,
        text=raw_text,
        ai_law_ref=resolution,
        filename=doc_filename
    )

    # Убираем статус ожидания и выводим ответ
    await status_msg.delete()
    
    response_text = (
        f"✅ *Ваше обращение успешно обработано!*\n\n"
        f"🏛 *Направление:* {category}\n\n"
        f"📜 *Правовое заключение ИИ:*\n{resolution}\n\n"
        f"📥 Ниже прикреплен готовый документ заявления для отправки в государственные органы через портал eOtinish."
    )
    await message.answer(response_text, parse_mode="Markdown")

    # Отправка сформированного документа
    if os.path.exists(doc_filename):
        input_file = types.FSInputFile(doc_filename)
        await message.answer_document(document=input_file, caption=f"Официальное_обращение_{category}.docx")
        os.remove(doc_filename) # Удаляем временный файл с сервера для гигиены данных

    await state.clear()
