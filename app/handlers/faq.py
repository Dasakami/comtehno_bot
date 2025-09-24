from aiogram import Router
from aiogram.types import Message

router = Router()
FAQ = {
    "Какие курсы есть?": "Frontend, Backend, React.js, HTML/CSS",
    "Сколько стоит обучение?": "Цена по запросу. Оставьте контакт и мы отправим прайс.",
    "Можно ли совмещать с учёбой/работой?": "Да, большинство курсов гибкие по времени.",
    "Выдаёте ли сертификаты?": "Да, по окончанию курса выдаём сертификат.",
    "Смогу ли я устроиться на работу после курса?": "Курсы ориентированы на трудоустройство, но итог зависит от вашего прогресса."
}

@router.message(lambda m: m.text and "Задать вопрос" in m.text)
async def on_faq(message: Message):
    text = "Частые вопросы:\n" + "\n".join(f"- {q}" for q in FAQ.keys())
    await message.answer(text)

@router.message(lambda m: m.text and m.text in FAQ)
async def get_answer(message: Message):
    await message.answer(FAQ[message.text])
