from config import LOG, LOG_GROUP_ID
import psutil
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


# 📌 Türkçe locale (hata yutmamak için try/except)
try:
    locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")
except Exception:
    # Sunucuda locale olmayabilir; varsayılan devam eder
    pass


# 📌 Sistem durumu
def get_system_status() -> Tuple[str, str, str]:
    """CPU, RAM ve disk yüzdelerini string olarak döndürür."""
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        return f"{cpu}%", f"{mem}%", f"{disk}%"
    except Exception as e:
        # Hata durumunda 0/0/0 döndürür ve hatayı loglar
        print(f"Sistem bilgisi alınamadı: {e}")
        return "0%", "0%", "0%"


# 📌 Grup bilgisi
async def get_chat_info(chat) -> Tuple[Union[int, str], str]:
    """Verilen chat objesinden üye sayısı ve grup linkini döndürür.

    Eğer üye sayısı alınamazsa 'Bilinmiyor' döner.
    Kullanıcı adı varsa @username döner.
    Yoksa özel grup davet linki üretmeye çalışır.
    """
    try:
        uye_sayisi = await app.get_chat_members_count(chat.id)
    except Exception:
        uye_sayisi = "Bilinmiyor"

    if getattr(chat, "username", None):
        chatusername = f"@{chat.username}"
    else:
        # Özel grup → davet linki almaya çalış
        try:
            chatusername = await app.export_chat_invite_link(chat.id)
        except Exception:
            chatusername = "Yok / Özel Grup"

    return uye_sayisi, chatusername


# 📌 Kullanıcı adı
def safe_username(user) -> str:
    """Kullanıcı username'ini güvenli şekilde döndürür; yoksa 'Yok' döner."""
    return f"@{user.username}" if getattr(user, "username", None) else "Yok"


# 📌 Tarih / Saat (Türkiye saati)
def get_turkish_datetime() -> str:
    istanbul = pytz.timezone("Europe/Istanbul")
    now = datetime.now(istanbul)
    tarih = now.strftime("%d %B %Y")
    saat = now.strftime("%H:%M:%S")
    gun = now.strftime("%A")
    return f"📅 {tarih}\n⏰ {saat} ({gun})"


# 📌 Log şablonu (hava durumu kaldırıldı)
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
    music_title: Optional[str] = None,
    music_artist: Optional[str] = None,
    tarih_saat: Optional[str] = None,
    action_type: str = "play",
) -> str:
    """Log metnini oluşturur. Hava durumu artık içermez."""
    music_info = ""
    if music_title:
        music_info += f"\n🎶 Şarkı   : {music_title}"
    if music_artist:
        music_info += f"\n🎤 Sanatçı: {music_artist}"

    sorgu = getattr(message, "text", None) or getattr(message, "caption", "Yok")
    if isinstance(sorgu, str) and len(sorgu) > 200:
        sorgu = sorgu[:200] + "..."

    baslik = "📥 Yeni Şarkı Sıraya Eklendi" if action_type == "queue" else "🔊 Yeni Müzik Oynatıldı"

    # Güvenli kullanıcı mention
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

🔎 Sorgu: {sorgu}{music_info}

💻 Sistem Durumu
├ 🖥️ CPU : {CPU}
├ 🧠 RAM : {RAM}
└ 💾 Disk: {DISK}

📊 Genel Durum
├ 🌐 Toplam Grup : {toplam_grup}
├ 🔊 Aktif Ses   : {aktif_sesli}
└ 🎥 Aktif Video : {aktif_video}
"""
    return log


# 📌 Ana fonksiyon
async def play_logs(
    message,
    streamtype: Optional[str] = None,
    music_title: Optional[str] = None,
    music_artist: Optional[str] = None,
    action_type: str = "play",
):
    """Logları oluşturur ve LOG_GROUP_ID'ye gönderir. Hata yönetimi içerir."""
    chat_id = message.chat.id
    user = message.from_user

    uye_sayisi, chatusername = await get_chat_info(message.chat)
    username = safe_username(user)

    # Veritabanı çağrıları
    toplam_grup = len(await get_served_chats())
    aktif_sesli = len(await get_active_chats())
    aktif_video = len(await get_active_video_chats())

    CPU, RAM, DISK = get_system_status()
    tarih_saat = get_turkish_datetime()

    if await is_on_off(LOG):
        logger_text = build_log_text(
            message,
            user,
            chatusername,
            username,
            uye_sayisi,
            CPU,
            RAM,
            DISK,
            toplam_grup,
            aktif_sesli,
            aktif_video,
            music_title,
            music_artist,
            tarih_saat=tarih_saat,
            action_type=action_type,
        )

        # LOG_GROUP_ID'ye gönder (aynı gruptan gönderme)
        if chat_id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    LOG_GROUP_ID,
                    logger_text,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(f"Log gönderilemedi: {e}")

            # Grup başlığını güncelle (opsiyonel, hata yutulur)
            try:
                current_title = f"🔊 Aktif Ses - {aktif_sesli}"
                chat_info = await app.get_chat(LOG_GROUP_ID)
                if getattr(chat_info, "title", None) != current_title:
                    await app.set_chat_title(LOG_GROUP_ID, current_title)
            except Exception:
                # Başlık güncellenemezse ilgilenme
                pass


# Eğer bu modül doğrudan çalıştırılırsa test amaçlı basit bir çıktı
if __name__ == "__main__":
    print("play_logs modülü yüklenmiştir. Hava durumu kaldırıldı ve özel grup linki eklenmiştir.")
