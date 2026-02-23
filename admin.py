from aiogram import Router, F
from aiogram.types import Message
from config import *
from database import *

router = Router()

@router.message(F.text.startswith("/give"))
async def give_bonus(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    _, user_id, amount = message.text.split()
    update_bonus(int(user_id), int(amount))
    await message.answer("Бонус берілді")
