from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from ArchMusic import app

@app.on_message(filters.command("atag") & filters.group & ~BANNED_USERS)
async def atag(client, message: Message):
    await message.reply("📨 Yöneticiler etiketleniyor... /cancel yazarak durdurabilirsin.")

    try:
        admins = []
        async for member in app.get_chat_administrators(message.chat.id):
            if not member.user.is_bot:
                admins.append(member)
    except Exception as e:
        return await message.reply(f"⚠️ Yöneticiler alınamadı:\n`{e}`")

    if not admins:
        return await message.reply("❗ Hiç yönetici bulunamadı.")

    etiketlenen = 0
    atilamayan = 0

    for admin in admins:
        try:
            await message.reply(
                f"👑 [{admin.user.first_name}](tg://user?id={admin.user.id})",
                quote=False
            )
            etiketlenen += 1
        except:
            atilamayan += 1

    await message.reply(
        f"✅ **Etiketleme Tamamlandı**\n"
        f"📍 Etiketlenen: {etiketlenen}\n"
        f"❌ Etiketlenemeyen: {atilamayan}"
    )
