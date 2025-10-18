from config import LOG, LOG_GROUP_ID
import psutil
import platform
import json
import time
import logging
from datetime import datetime
import pytz
import locale
from typing import Optional, Tuple, Union

from ArchMusic import app
from ArchMusic.utils.database import is_on_off
from ArchMusic.utils.database.memorydatabase import (
    get_active_chats, get_active_video_chats
)
from ArchMusic.utils.database import get_served_chats

# 📌 Türkçe locale
try:
    locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")
except Exception:
    pass

# 📌 Başlangıç zamanı (uptime hesaplamak için)
BOT_START_TIME = time.time()

# 📋 Loglama ayarları
logging.basicConfig(
    filename="bot_play_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ------------------------------------------------
# 🔧 Yardımcı Fonksiyonlar
# ------------------------------------------------

def get_system_status() -> Tuple[str, str, str]:
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        return f"{cpu}%", f"{mem}%", f"{disk}%"
    except Exception as e:
        print(f"Sistem bilgisi alınamadı: {e}")
        return "0%", "0%", "0%"

def get_system_details() -> str:
    system = platform.system()
    release = platform.release()
    cores = psutil.cpu_count(logical=True)
    return f"{system} {release} | {cores} Çekirdek"

def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            t = temps["coretemp"][0].current
            return f"{t}°C"
    except Exception:
        pass
    return "N/A"

def get_io_status():
    try:
        net = psutil.net_io_counters()
        sent = round(net.bytes_sent / 1024 / 1024, 2)
        recv = round(net.bytes_recv / 1024 / 1024, 2)
        return f"⬆️ {sent}MB / ⬇️ {recv}MB"
    except Exception:
        return "N/A"

def warn_high_usage(value_str: str) -> str:
    value = float(value_str.replace("%", ""))
    if value > 85:
        return "🔥"
    elif value > 70:
        return "⚠️"
    return "✅"

def get_uptime() -> str:
    uptime_seconds = int(time.time() - BOT_START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

async def get_ping() -> str:
    start = time.time()
    await app.get_me()
    ping = (time.time() - start) * 1000
    return f"{ping:.0f} ms"

def safe_username(user) -> str:
    return f"@{user.username}" if getattr(user, "username", None) else "Yok"

def get_turkish_datetime() -> str:
    istanbul = pytz.timezone("Europe/Istanbul")
    now = datetime.now(istanbul)
    tarih = now.strftime("%d %B %Y")
    saat = now.strftime("%H:%M:%S")
    gun = now.strftime("%A")
    return f"📅 {tarih}\n⏰ {saat} ({gun})"

def write_log_to_file(log_text: str):
    try:
        logging.info(log_text)
    except Exception as e:
        print(f"Log dosyasına yazılamadı: {e}")

def mask_sensitive_data(text: str) -> str:
    return text.replace("@", "@*").replace(str(LOG_GROUP_ID), "******")

def increase_query_count():
    try:
        data = json.load(open("query_count.json", "r"))
    except FileNotFoundError:
        data = {"count": 0}
    data["count"] += 1
    json.dump(data, open("query_count.json", "w"))
    return data["count"]

def detect_source(message) -> str:
    if message.text and message.text.startswith("/"):
        return "Komut"
    elif getattr(message, "via_bot", None):
        return "Inline"
    elif getattr(message, "entities", None):
        return "Bağlantı"
    return "Manuel"

# ------------------------------------------------
# 🔧 Ana Fonksiyonlar
# ------------------------------------------------

async def get_chat_info(chat) -> Tuple[Union[int, str], str]:
    try:
        uye_sayisi = await app.get_chat_members_count(chat.id)
    except Exception:
        uye_sayisi = "Bilinmiyor"

    if getattr(chat, "username", None):
        chatusername = f"@{chat.username}"
    else:
        try:
            chatusername = await app.export_chat_invite_link(chat.id)
        except Exception:
            chatusername = "Yok / Özel Grup"

    return uye_sayisi, chatusername


def build_log_text(
    message,
    user,
    chatusername: str,
    username: str,
    uye_sayisi,
    CPU: str,
    RAM: str,
    DISK: str,
    toplam_grup: int,
    aktif_sesli: int,
    aktif_video: int,
    uptime: str,
    ping: str,
    system_info: str,
    cpu_temp: str,
    net_io: str,
    query_count: int,
    tarih_saat: Optional[str] = None,
    action_type: str = "play",
    music_title: Optional[str] = None,
    music_artist: Optional[str] = None,
) -> str:

    music_info = ""
    if music_title:
        music_info += f"\n🎶 Şarkı   : {music_title}"
    if music_artist:
        music_info += f"\n🎤 Sanatçı: {music_artist}"

    sorgu = getattr(message, "text", None) or getattr(message, "caption", "Yok")
    if isinstance(sorgu, str) and len(sorgu) > 200:
        sorgu = sorgu[:200] + "..."

    baslik = "📥 Yeni Şarkı Sıraya Eklendi" if action_type == "queue" else "🔊 Yeni Müzik Oynatıldı"

    user_mention = getattr(user, "mention", None)
    if not user_mention:
        first = getattr(user, "first_name", "Bilinmiyor")
        uid = getattr(user, "id", "Bilinmiyor")
        user_mention = f"{first} (id: {uid})"

    chat_title = getattr(message.chat, "title", "Özel Chat")

    log = f"""
{baslik}

🕒 Tarih/Saat:
{tarih_saat}

📚 Grup: {chat_title} [{message.chat.id}]
🔗 Grup Linki: {chatusername}
👥 Üye Sayısı: {uye_sayisi}

👤 Kullanıcı: {user_mention}
✨ Kullanıcı Adı: {username}
🔢 Kullanıcı ID: {getattr(user, 'id', 'Bilinmiyor')}
🔍 Kaynak: {detect_source(message)}

🔎 Sorgu: {sorgu}{music_info}

💻 Sistem Durumu
├ 🧩 Sistem: {system_info}
├ 🖥️ CPU : {CPU} {warn_high_usage(CPU)}
├ 🧠 RAM : {RAM} {warn_high_usage(RAM)}
├ 💾 Disk: {DISK} {warn_high_usage(DISK)}
├ 🌡️ CPU Sıcaklığı: {cpu_temp}
├ 🌐 Ağ Kullanımı : {net_io}
└ ⏳ Uptime: {uptime}

⚡ Ping: {ping}

📊 Genel Durum
├ 🌐 Toplam Grup : {toplam_grup}
├ 🔊 Aktif Ses   : {aktif_sesli}
├ 🎥 Aktif Video : {aktif_video}
└ 📈 Toplam Sorgu: {query_count}
"""
    return log


async def play_logs(
    message,
    streamtype: Optional[str] = None,
    music_title: Optional[str] = None,
    music_artist: Optional[str] = None,
    action_type: str = "play",
):
    chat_id = message.chat.id
    user = message.from_user

    uye_sayisi, chatusername = await get_chat_info(message.chat)
    username = safe_username(user)

    toplam_grup = len(await get_served_chats())
    aktif_sesli = len(await get_active_chats())
    aktif_video = len(await get_active_video_chats())

    CPU, RAM, DISK = get_system_status()
    uptime = get_uptime()
    ping = await get_ping()
    system_info = get_system_details()
    cpu_temp = get_cpu_temp()
    net_io = get_io_status()
    query_count = increase_query_count()
    tarih_saat = get_turkish_datetime()

    if await is_on_off(LOG):
        logger_text = build_log_text(
            message, user, chatusername, username, uye_sayisi,
            CPU, RAM, DISK, toplam_grup, aktif_sesli, aktif_video,
            uptime, ping, system_info, cpu_temp, net_io,
            query_count, tarih_saat, action_type, music_title, music_artist
        )

        logger_text = mask_sensitive_data(logger_text)
        write_log_to_file(logger_text)

        if chat_id != LOG_GROUP_ID:
            try:
                await app.send_message(LOG_GROUP_ID, logger_text, disable_web_page_preview=True)
            except Exception as e:
                print(f"Log gönderilemedi: {e}")

            try:
                current_title = f"🔊 Aktif Ses - {aktif_sesli}"
                chat_info = await app.get_chat(LOG_GROUP_ID)
                if getattr(chat_info, "title", None) != current_title:
                    await app.set_chat_title(LOG_GROUP_ID, current_title)
            except Exception:
                pass


if __name__ == "__main__":
    print("✅ play_logs modülü (v2) yüklendi — Gelişmiş loglama, uptime, ping ve sistem bilgisi eklendi.")
