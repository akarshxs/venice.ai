from aiogram import Router, types
from aiogram.filters import Command
from db import set_admin, set_premium, get_stats, get_all_users

router = Router()

def admin_only(func):
    async def wrapper(m: types.Message):
        from db import get_user
        user = get_user(m.from_user.id)
        if not user[4]:
            await m.answer("🚫 Admin only.")
            return
        return await func(m)
    return wrapper

@router.message(Command("admin"))
@admin_only
async def admin(m: types.Message):
    await m.answer("🔧 Admin Panel\n/grantpremium ID\n/revokepremium ID\n/addadmin ID\n/stats\n/broadcast")

@router.message(Command("grantpremium"))
@admin_only
async def grant(m: types.Message):
    uid = int(m.text.split()[1])
    set_premium(uid, 1)
    await m.answer("✅ Premium granted.")

@router.message(Command("revokepremium"))
@admin_only
async def revoke(m: types.Message):
    uid = int(m.text.split()[1])
    set_premium(uid, 0)
    await m.answer("❌ Premium revoked.")

@router.message(Command("addadmin"))
@admin_only
async def addadmin(m: types.Message):
    uid = int(m.text.split()[1])
    set_admin(uid, 1)
    await m.answer("👑 Admin added.")

@router.message(Command("stats"))
@admin_only
async def stats(m: types.Message):
    total, premium = get_stats()
    await m.answer(f"📊 Users: {total}\nPremium: {premium}")

@router.message(Command("broadcast"))
@admin_only
async def broadcast(m: types.Message):
    users = get_all_users()
    sent = 0
    for u in users:
        try:
            await m.bot.send_message(u[0], "📢 Admin Broadcast:\n" + m.text.replace("/broadcast", ""))
            sent += 1
        except:
            pass
    await m.answer(f"✅ Broadcast sent to {sent} users.")
