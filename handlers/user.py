from aiogram import Router, types
from aiogram.filters import Command
from db import add_user, get_user
from ai.venice import ask_venice

router = Router()

@router.message(Command("start"))
async def start(m: types.Message):
    add_user(m.from_user.id, m.from_user.username)
    await m.answer("👋 Welcome! Use /profile, /buy, or just chat with me.")

@router.message(Command("profile"))
async def profile(m: types.Message):
    user = get_user(m.from_user.id)
    await m.answer(f"""👤 Profile
ID: {user[0]}
Username: {user[1]}
Premium: {'Yes' if user[3] else 'No'}
Admin: {'Yes' if user[4] else 'No'}""")

@router.message(Command("buy"))
async def buy(m: types.Message):
    await m.answer("💎 Premium Plans:\n$5/month\nContact admin for approval.")

@router.message()
async def chat(m: types.Message):
    user = get_user(m.from_user.id)
    if not user[3]:
        await m.answer("❌ Free users have limited access. Use /buy.")
        return

    await m.answer("🤖 Thinking...")
    reply = await ask_venice(m.from_user.id, m.text)
    await m.answer(reply)
