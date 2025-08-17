from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from strings import get_command
from ArchMusic import app
from ArchMusic.misc import SUDOERS

import speedtest
import asyncio
import concurrent.futures

# Hız testi komutu
SPEEDTEST_COMMAND = get_command("speedtest")  # strings/command içinde "speedtest": "/speedtest" ekli olmalı

# Thread pool executor, speedtest işlemini ayrı thread’de çalıştıracak
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

def run_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 10**6  # Mbps
    upload_speed = st.upload() / 10**6      # Mbps
    ping_result = st.results.ping
    return download_speed, upload_speed, ping_result

@app.on_message(filters.command(SPEEDTEST_COMMAND) & filters.user(SUDOERS))
async def speed_test(client, message: Message):
    msg = await message.reply_text("Hız testi başlatılıyor... ⏳")
    
    # Emoji ve renkli loading bar animasyonu
    loading_frames = [
        "🟩□□□□□□□□□□ 10%",
        "🟩🟩□□□□□□□□ 20%",
        "🟩🟩🟩□□□□□□ 30%",
        "🟩🟩🟩🟩□□□□□ 40%",
        "🟩🟩🟩🟩🟩□□□□ 50%",
        "🟩🟩🟩🟩🟩🟩□□□ 60%",
        "🟩🟩🟩🟩🟩🟩🟩□□ 70%",
        "🟩🟩🟩🟩🟩🟩🟩🟩□ 80%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩 90%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%"
    ]
    
    # Animasyon döngüsü
    for frame in loading_frames:
        await asyncio.sleep(0.3)
        await msg.edit_text(f"Hız testi başlatılıyor... ⏳\n{frame}")
    
    # speedtest işlemini thread’de çalıştır
    loop = asyncio.get_event_loop()
    download_speed, upload_speed, ping_result = await loop.run_in_executor(executor, run_speedtest)

    result_text = (
        f"**Hız Testi Sonuçları:**\n"
        f"Ping: {ping_result} ms\n"
        f"Download: {download_speed:.2f} Mbps\n"
        f"Upload: {upload_speed:.2f} Mbps"
    )

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Tekrar Test Et", callback_data="speed_test_again")]]
    )

    await msg.edit_text(result_text, reply_markup=keyboard)

@app.on_callback_query(filters.regex("speed_test_again") & filters.user(SUDOERS))
async def speed_test_again(client, callback_query):
    await callback_query.answer()
    await speed_test(client, callback_query.message)


