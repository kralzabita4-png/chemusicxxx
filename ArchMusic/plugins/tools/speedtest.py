import asyncio
import speedtest
from pyrogram import filters
from strings import get_command
from ArchMusic import app
from ArchMusic.misc import SUDOERS

# Komutlar
HIZ_TESTI_KOMUTU = get_command("SPEEDTEST_COMMAND")


# Hız testi yapan fonksiyon
async def hiz_testi(mesaj):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        await mesaj.edit("<b>⇆ 𝖬𝖺𝖫𝗓𝖾𝗆𝖾 𝖳𝖾𝖲𝗍𝗂 𝖸𝖴𝗋𝗎𝗇𝗂𝗒𝗈𝗋 ...</b>")
        
        # İndir ve yükleme hızlarını ölç
        test.download()
        await mesaj.edit("<b>⇆ 𝖸𝖴𝗄𝗅𝖾𝗆𝖾 𝖧𝗂𝗓𝗂 𝖬𝖾𝗅𝗈𝗍𝗋 ...</b>")
        test.upload()
        
        test.results.share()
        sonuc = test.results.dict()
        await mesaj.edit("<b>↻ 𝖧𝗂𝗓 𝖳𝖾𝗌𝗍𝗂 𝖲𝗈𝗇𝖼𝗎𝗅𝗋𝗎 𝖲𝗁𝖺𝗋𝗂𝗇𝗀 ...</b>")
    except Exception as e:
        return await mesaj.edit(str(e))
    return sonuc


# Hızı görsel olarak emoji ile göster (otomatik ölçekli)
def hiz_grafik_otomatik(indir_hizi, yukle_hizi, bar_length=20):
    """indir_hizi ve yukle_hizi: Mbps cinsinden hızlar"""
    max_speed = max(indir_hizi, yukle_hizi, 1)  # 0 bölme hatası için 1
    indir_dolu = int((indir_hizi / max_speed) * bar_length)
    yukle_dolu = int((yukle_hizi / max_speed) * bar_length)
    indir_bar = "🟩" * indir_dolu + "⬜" * (bar_length - indir_dolu)
    yukle_bar = "🟩" * yukle_dolu + "⬜" * (bar_length - yukle_dolu)
    return indir_bar, yukle_bar


# Bot komutu
@app.on_message(filters.command(HIZ_TESTI_KOMUTU) & SUDOERS)
async def hiz_testi_fonksiyonu(client, mesaj):
    m = await mesaj.reply_text("» 𝖧𝗂𝗓 𝖳𝖾𝗌𝗍𝗂 𝖱𝗎𝗇𝗇𝗂𝗇𝗀 ...")
    sonuc = await hiz_testi(m)
    
    if not sonuc:
        return

    # Mbps olarak dönüştür
    indir_hizi = round(sonuc['download'] / 10**6, 2)  # Mbps
    yukle_hizi = round(sonuc['upload'] / 10**6, 2)    # Mbps
    ping_ms = round(sonuc['ping'], 2)                 # Ping ms

    # Emoji ile otomatik ölçekli grafik
    indir_grafik, yukle_grafik = hiz_grafik_otomatik(indir_hizi, yukle_hizi)

    # Google Maps linkleri
    client_lat = sonuc['client']['lat']
    client_lon = sonuc['client']['lon']
    server_lat = sonuc['server']['lat']
    server_lon = sonuc['server']['lon']

    client_map = f"https://www.google.com/maps/search/?api=1&query={client_lat},{client_lon}"
    server_map = f"https://www.google.com/maps/search/?api=1&query={server_lat},{server_lon}"

    cikti = f"""✯ <b>𝖧𝗂𝗓 𝖳𝖾𝗌𝗍𝗂 𝖲𝗈𝗇𝖼𝗎𝗅𝗋𝗎</b> ✯

<u><b>𝖬𝖴𝖲𝗍𝖾𝗋𝗂 :</b></u>
<b>» 𝖸𝗌𝗉 :</b> {sonuc['client']['isp']}
<b>» 𝖴𝗅𝗄𝗲 :</b> {sonuc['client']['country']}
<b>» 🌐 Konum :</b> <a href="{client_map}">Haritada Göster</a>

<u><b>𝖲𝖾𝗋𝗏𝖾𝗋 :</b></u>
<b>» 𝖠𝖣𝗂 :</b> {sonuc['server']['name']}
<b>» 𝖴𝗅𝗄𝗲 :</b> {sonuc['server']['country']}, {sonuc['server']['cc']}
<b>» 𝖲𝗉𝗈𝗇𝗌𝗈𝗋 :</b> {sonuc['server']['sponsor']}
<b>» 𝖦𝗎𝗈𝗋𝗀𝗎𝗇𝗀 :</b> {sonuc['server']['latency']} ms
<b>» 𝖯𝗂𝗇𝗀 :</b> {ping_ms} ms
<b>» 🌐 Konum :</b> <a href="{server_map}">Haritada Göster</a>

<b>» 𝖨𝗇𝗗𝗂𝗋𝗆𝗂𝗇 𝖧𝗂𝗓 :</b> {indir_hizi} Mbps {indir_grafik}
<b>» 𝖸𝗎𝗄𝗅𝖾𝗆𝖾 𝖧𝗂𝗓 :</b> {yukle_hizi} Mbps {yukle_grafik}
"""

    msg = await app.send_photo(
        chat_id=mesaj.chat.id, photo=sonuc["share"], caption=cikti, parse_mode="HTML"
    )
    await m.delete()
    
