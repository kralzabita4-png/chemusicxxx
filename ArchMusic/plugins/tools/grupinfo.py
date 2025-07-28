from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_GROUP_ID  # -100 ile başlayan gerçek ID
from ArchMusic import app
import traceback


# ✅ Log mesajı oluştur
async def create_log_message(event_type: str, chat, user):
    emoji = "✅" if event_type == "joined" else "🚫"
    title = "**Bot Gruba Eklendi**" if event_type == "joined" else "**Bot Gruptan Çıkarıldı**"
    action_by = user.mention if user and hasattr(user, "mention") else "Bilinmeyen"
    members_count = await app.get_chat_members_count(chat.id)

    message = (
        f"{emoji} {title}\n\n"
        f"📌 **Grup:** `{chat.title}`\n"
        f"🆔 **Grup ID:** `{chat.id}`\n"
        f"👥 **Üye Sayısı:** `{members_count}`\n"
        f"👤 **İşlemi Yapan:** {action_by}\n"
    )

    if chat.username:
        message += f"\n🔗 [@{chat.username}](https://t.me/{chat.username})"

    return message


# ✅ Bot gruba eklendiğinde log gönder
@app.on_message(filters.new_chat_members)
async def bot_added_handler(client: Client, message: Message):
    try:
        bot_user = await app.get_me()
        for member in message.new_chat_members:
            if member.id == bot_user.id:
                print(f"[DEBUG] Bot gruba eklendi: {message.chat.id}")
                log_text = await create_log_message("joined", message.chat, message.from_user)
                chat_id = message.chat.id

                if message.chat.username:
                    url = f"https://t.me/{message.chat.username}"
                else:
                    url = f"https://t.me/c/{str(chat_id)[4:]}/1"

                buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton("📂 Gruba Git", url=url)]
                ])

                await app.send_message(LOG_GROUP_ID, log_text, reply_markup=buttons)
                print(f"[LOG] Log gönderildi: {chat_id}")
                break

    except Exception as e:
        print(f"[HATA] Bot gruba eklendiğinde log gönderilemedi:\n{e}")
        traceback.print_exc()


# ✅ Bot gruptan çıkarıldığında log gönder
@app.on_message(filters.left_chat_member)
async def bot_removed_handler(client: Client, message: Message):
    try:
        bot_user = await app.get_me()
        if message.left_chat_member.id == bot_user.id:
            print(f"[DEBUG] Bot gruptan çıkarıldı: {message.chat.id}")
            log_text = await create_log_message("left", message.chat, message.from_user)
            chat_id = message.chat.id

            if message.chat.username:
                url = f"https://t.me/{message.chat.username}"
            else:
                url = f"https://t.me/c/{str(chat_id)[4:]}/1"

            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("📁 Grup Bilgisi", url=url)]
            ])

            await app.send_message(LOG_GROUP_ID, log_text, reply_markup=buttons)
            print(f"[LOG] Log gönderildi: {chat_id}")

    except Exception as e:
        print(f"[HATA] Bot gruptan çıkarıldığında log gönderilemedi:\n{e}")
        traceback.print_exc()


# ✅ Manuel log testi için komut
@app.on_message(filters.command("logtest") & filters.private)
async def log_test_handler(client: Client, message: Message):
    try:
        test_text = "✅ Bu bir test log mesajıdır."
        await app.send_message(LOG_GROUP_ID, test_text)
        await message.reply("✅ Log gruba başarıyla gönderildi.")
    except Exception as e:
        print(f"[HATA] Log test mesajı gönderilemedi:\n{e}")
        traceback.print_exc()
        await message.reply("❌ Log gruba gönderilemedi.")
