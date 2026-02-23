from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from database import *
from config import *

router = Router()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎥 Видео"), KeyboardButton(text="📷 Фото")],
        [KeyboardButton(text="💰 Бонус"), KeyboardButton(text="👥 Реферал")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "/start")
async def start(message: Message):
    args = message.text.split()

    invited_by = None
    if len(args) > 1:
        invited_by = int(args[1])

    new = add_user(message.from_user.id, invited_by)

    if new and invited_by:
        update_bonus(invited_by, 4)
        add_referral(invited_by)
        await message.bot.send_message(
            invited_by,
            "🎉 Сіз адам шақырдыңыз! 4 бонус алдыңыз!"
        )

    await message.answer(
        "Қош келдіңіз! Сізге 6 бонус берілді 🎁",
        reply_markup=menu
    )

@router.message(F.text == "💰 Бонус")
async def bonus(message: Message):
    b = get_bonus(message.from_user.id)
    if b <= 0:
        link = f"https://t.me/{BOT_USERNAME}?start={message.from_user.id}"
        await message.answer(
            f"Бонус бітті!\nАдам шақырыңыз:\n{link}"
        )
    else:
        await message.answer(f"Сізде {b} бонус бар")
