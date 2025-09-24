from aiogram import Router, types
from app.utils import validate_phone
from app.db import AsyncSessionLocal
from app.crud import create_lead
from app.schemas import LeadCreate
from app.config import ADMIN_CHAT_IDS

router = Router()
_pending_signup: dict[int, str] = {}  


@router.callback_query(lambda c: c.data and c.data.startswith("signup:"))
async def signup_callback(query: types.CallbackQuery):
    course = query.data.split(":", 1)[1]
    chat_id = query.from_user.id
    _pending_signup[chat_id] = course
    await query.message.answer(
        "Отправьте данные для записи: Имя, телефон, формат(онлайн/офлайн)."
    )
    await query.answer()


@router.message(lambda m: "," in m.text and m.from_user.id in _pending_signup)
async def receive_signup(message: types.Message):
    parts = [p.strip() for p in message.text.split(",")]
    if len(parts) < 2:
        return await message.reply("Неверный формат. Нужно: Имя, телефон, формат(онлайн/офлайн).")

    name = parts[0]
    phone = validate_phone(parts[1])
    if not phone:
        return await message.reply("Невалидный номер")

    fmt = parts[2] if len(parts) > 2 else None
    course = _pending_signup.pop(message.from_user.id)


    payload = LeadCreate(name=name, phone=phone, course=course, format=fmt, source="signup")
    async with AsyncSessionLocal() as db:
        await create_lead(db, payload)

    await message.answer("Спасибо! Мы скоро свяжемся с вами 📞")

    for admin in ADMIN_CHAT_IDS:
        await message.bot.send_message(
            admin, f"Новая заявка: {name} | {phone} | {course} | {fmt}"
        )
