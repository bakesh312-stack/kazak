import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
from config import *
from database import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

CHANNEL = "@СЕНІҢ_КАНАЛ"

async def check_sub(user_id):
    member = await bot.get_chat_member(CHANNEL, user_id)
    return member.status in ["member", "administrator", "creator"]

@dp.message(Command("start"))
async def start(message: types.Message):
    args = message.text.split()
    invited_by = int(args[1]) if len(args) > 1 else None

    if not await check_sub(message.from_user.id):
        await message.answer("Алдымен каналға тіркеліңіз!")
        return

    new = add_user(message.from_user.id, invited_by)

    if new and invited_by:
        update_bonus(invited_by, 4)
        await bot.send_message(invited_by, "Сіз 4 бонус алдыңыз!")

    await message.answer("Сізге 6 бонус берілді!")

@dp.message()
async def menu(message: types.Message):
    if message.text == "💰 Бонус":
        b = get_bonus(message.from_user.id)
        await message.answer(f"Сізде {b} бонус бар")

async def on_startup(app):
    await bot.set_webhook(os.getenv("WEBHOOK_URL"))

async def on_shutdown(app):
    await bot.delete_webhook()

app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

web.run_app(app, port=int(os.getenv("PORT", 8000)))
