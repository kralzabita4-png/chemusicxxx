import random
import asyncio
from collections import defaultdict
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from ArchMusic import app

# ✅ Söz listesi (dilersen genişletebilirsin)
SOZ_LISTESI = [
    "Hayal gücü bilgiden daha önemlidir. – Albert Einstein",
    "Yavaş git ama asla durma. – Confucius",
    "Her şey seninle başlar.",
    "Gülüşün bu dünyaya armağan 😄",
    "Senin enerjin etrafı aydınlatıyor 💡",
    "Sen anlatılmaz, yaşanırsın 💌",
    "Bir tebessümün bile yeter 🌸",
    "Seninle geçirilen anlar unutulmaz 📸",
    "Sen sadece bir isim değil, bir anlam taşıyorsun 🧡"
]

# ✅ İptal listesi (kullanıcı bazlı)
cancel_users = defaultdict(set)

# ✅ /cancel komutu
@app.on_message(filters.command("cancel") & filters.group & ~BANNED_USERS)
async def cancel_soz(client, message: Message):
    cancel_users[message.chat.id].add(message.from_user.id)
    await message.reply("❌ Etiketleme işlemi iptal edildi.")

# ✅ /soz komutu
@app.on_message(filters.command("soz") & filters.group & ~BANNED_USERS)
async def soz_etiketle(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id in cancel_users[chat_id]:
        cancel_users[chat_id].remove(user_id)
        return await message.reply("⛔ Zaten iptal edilmişti.")

    await message.reply("📨 Üyelere söz gönderiliyor... Durdurmak için `/cancel` yaz.")

    try:
        members = app.iter_chat_members(chat_id)
    except Exception as e:
        return await message.reply(f"⚠️ Üye listesi alınamadı:\n`{e}`")

    etiketlenen = 0
    atilamayan = 0

    async for member in members:
        if member.user.is_bot:
            continue

        if user_id in cancel_users[chat_id]:
            cancel_users[chat_id].remove(user_id)
            return await message.reply("🛑 Etiketleme işlemi iptal edildi.")

        soz = random.choice(SOZ_LISTESI)
        try:
            await message.reply(
                f"👤 [{member.user.first_name}](tg://user?id={member.user.id})\n\n📝 _{soz}_",
                quote=False
            )
            etiketlenen += 1
        except:
            atilamayan += 1

        await asyncio.sleep(1.5)  # çok hızlı olmasın, flood koruması

    await message.reply(
        f"✅ **Etiketleme Bitti**\n"
        f"👥 Etiketlenen: {etiketlenen}\n"
        f"❌ Atılamayan: {atilamayan}\n"
        f"🎯 Toplam: {etiketlenen + atilamayan}"
    )
