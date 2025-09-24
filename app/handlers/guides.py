from aiogram import Router
from aiogram.types import Message, CallbackQuery
from app.keyboards import guide_inline
from app.config import STATIC_DIR, ADMIN_CHAT_IDS
from app.schemas import LeadCreate
from app.crud import create_lead
from app.db import AsyncSessionLocal
from app.utils import validate_phone
import os
from aiogram.types import FSInputFile
router = Router()
_pending_guide: dict[int, str] = {}  

@router.message(lambda m: m.text and "Получить бесплатный гайд" in m.text)
async def ask_guide(message: Message):
    await message.answer(
        "Выберите гайд:",
        reply_markup=guide_inline()  
    )

@router.callback_query(lambda c: c.data and c.data.startswith("guide:"))
async def guide_cb(query: CallbackQuery):
    filename = query.data.split(":", 1)[1]
    chat_id = query.from_user.id
    _pending_guide[chat_id] = filename
    await query.message.answer(
        "Отправьте данные: Имя, телефон, email (опционально). Формат через запятую."
    )
    await query.answer()

@router.message(lambda m: "," in m.text and m.from_user.id in _pending_guide)
async def receive_lead(message: Message):
    parts = [p.strip() for p in message.text.split(",")]
    if len(parts) < 2:
        return await message.reply(
            "Неверный формат. Нужно: Имя, телефон, email (опционално)"
        )

    name = parts[0]
    raw_phone = parts[1]
    phone = validate_phone(raw_phone)
    if not phone:
        return await message.reply(
            "Невалидный номер. Укажи в международном формате или попробуй +996..."
        )

    email = parts[2] if len(parts) > 2 else None
    filename = _pending_guide.pop(message.from_user.id, "backend_guide.pdf")

    
    payload = LeadCreate(name=name, phone=phone, email=email, source="guide", note=filename)
    async with AsyncSessionLocal() as db:
        await create_lead(db, payload)

    
    path = os.path.join(STATIC_DIR, "guieds", filename)  
    if os.path.exists(path) and os.path.getsize(path) > 0:
        file = FSInputFile(path) 
        await message.answer_document(file)
    else:
        await message.answer("Гайд не найден или пустой, мы свяжемся с вами.")


    for admin in ADMIN_CHAT_IDS:
        await message.bot.send_message(
            admin,
            f"Новый лид (гайд): {name} | {phone} | {email or '-'} | {filename}"
        )