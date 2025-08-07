from pyrogram import filters
import psutil
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ArchMusic import app
from config import SUDOERS, LOG_GROUP_ID
from ArchMusic.utils.database import (
    get_served_chats,
    get_served_users,
    get_queries,
    get_active_chats,
    get_active_video_chats,
)


# Ortak istatistik metni oluşturucu
async def generate_stats_text():
    gruplar = await get_served_chats()
    toplam_grup = len(gruplar)
    acik_grup = 0
    gizli_grup = 0

    for chat in gruplar:
        try:
            chat_info = await app.get_chat(chat["chat_id"])
            if chat_info.username:
                acik_grup += 1
            else:
                gizli_grup += 1
        except:
            gizli_grup += 1

    toplam_kullanici = len(await get_served_users())
    toplam_sorgu = await get_queries()
    aktif_sesli = len(await get_active_chats())
    aktif_video = len(await get_active_video_chats())

    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    CPU = f"{cpu}%"
    RAM = f"{ram}%"
    DISK = f"{disk}%"

    text = (
        f"📊 **Bot İstatistikleri**\n\n"
        f"👥 **Toplam Grup:** `{toplam_grup}`\n"
        f"├ 🌐 **Açık Grup:** `{acik_grup}`\n"
        f"└ 🔒 **Gizli Grup:** `{gizli_grup}`\n\n"
        f"👤 **Toplam Kullanıcı:** `{toplam_kullanici}`\n"
        f"🔍 **Toplam Müzik Sorgusu:** `{toplam_sorgu}`\n\n"
        f"🔊 **Aktif Sesli Sohbetler:** `{aktif_sesli}`\n"
        f"🎥 **Aktif Video Sohbetler:** `{aktif_video}`\n\n"
        f"💻 **Sistem Durumu**\n"
        f"├ 🖥️ CPU: `{CPU}`\n"
        f"├ 🧠 RAM: `{RAM}`\n"
        f"└ 💾 Disk: `{DISK}`"
    )
    return text


# Komut: /istatistik, /durum, /veri (SUDOERS için)
@app.on_message(filters.command(["istatistik", "durum", "veri"]) & filters.user(SUDOERS))
async def genel_istatistik(_, message):
    try:
        text = await generate_stats_text()

        chat = message.chat
        user = message.from_user

        if chat.username:
            grup_link = f"https://t.me/{chat.username}"
        else:
            grup_link = "Gizli Grup"

        grup_id = chat.id
        kullanici_adi = f"@{user.username}" if user.username else "Yok"
        kullanici_id = user.id

        ek_bilgiler = (
            f"\n\n🔗 Grup Linki: {grup_link}"
            f"\n🆔 Grup ID: `{grup_id}`"
            f"\n👤 Kullanıcı Adı: {kullanici_adi}"
            f"\n🆔 Kullanıcı ID: `{kullanici_id}`"
        )

        await message.reply_text(text + ek_bilgiler, quote=True)

        # Log kanalına da gönder
        try:
            await app.send_message(
                LOG_GROUP_ID,
                f"📥 `/istatistik` komutu çalıştırıldı.\n\n{text + ek_bilgiler}",
            )
        except Exception as log_err:
            print(f"Log kanalına gönderilemedi: {log_err}")

    except Exception as e:
        await message.reply_text(f"❌ Bir hata oluştu:\n`{e}`")


# Günlük otomatik istatistik gönderici
async def gonder_istatistik_log():
    try:
        text = await generate_stats_text()
        await app.send_message(LOG_GROUP_ID, f"📆 **Günlük Otomatik İstatistik**\n\n{text}")
    except Exception as e:
        print(f"🚨 Günlük istatistik gönderilemedi: {e}")


# Scheduler başlatıcı (günde 1 kez 12:00'de çalıştırır)
def start_scheduler():
    scheduler = AsyncIOScheduler(timezone="Europe/Istanbul")
    scheduler.add_job(gonder_istatistik_log, trigger="cron", hour=12, minute=0)
    scheduler.start()
