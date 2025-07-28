from pyrogram import Client
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_GROUP_ID
from ArchMusic import app


async def new_message(chat_id: int, message: str, reply_markup=None):
    await app.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


@app.on_chat_member_updated()
async def on_chat_member_update(client: Client, update: ChatMemberUpdated):
    old = update.old_chat_member
    new = update.new_chat_member
    user = update.new_chat_member.user
    chat = update.chat
    actor = update.from_user

    actor_name = actor.mention if actor else "Bilinmiyor"
    actor_id = actor.id if actor else None
    user_name = user.mention if user else "Bilinmiyor"
    title = chat.title
    chat_id = chat.id

    action = None

    # Bot olayları
    if user.is_self:
        if new.status == "kicked":
            action = "Bot gruptan **banlandı**"
        elif old.status == "kicked" and new.status == "member":
            action = "Bot gruba **geri alındı** (ban kaldırıldı)"
    else:
        # Kullanıcı banlandı
        if new.status == "kicked":
            action = f"{user_name} gruptan **banlandı**"
        # Kullanıcı ban kaldırıldı
        elif old.status == "kicked" and new.status == "member":
            action = f"{user_name} gruba **geri alındı** (ban kaldırıldı)"
        # Kullanıcı yönetici yapıldı
        elif old.status == "member" and new.status == "administrator":
            action = f"{user_name} **yönetici yapıldı**"
        # Kullanıcı yöneticilikten alındı
        elif old.status == "administrator" and new.status == "member":
            action = f"{user_name} **yöneticilikten alındı**"
        # Kullanıcı gruptan çıkarıldı (left)
        elif new.status == "left":
            action = f"{user_name} gruptan **ayrıldı veya çıkarıldı**"

    if action:
        text = (
            f"<u>#ÜyelikGüncellemesi</u>\n\n"
            f"**Grup:** {title}\n"
            f"**Grup ID:** `{chat_id}`\n"
            f"**İşlem:** {action}\n"
            f"**İşlemi Yapan:** {actor_name}"
        )

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(actor_name, user_id=actor_id)]] if actor_id else []
        )

        await new_message(LOG_GROUP_ID, text, reply_markup)
