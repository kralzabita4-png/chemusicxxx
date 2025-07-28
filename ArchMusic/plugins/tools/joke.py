import random
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from ArchMusic import app

# 50 esprili şaka
JOKES = [
    "😂 Matematik kitabı neden üzgündü? Çünkü çok problemi vardı!",
    "🤣 En tembel hayvan hangisidir? Üşengeç kanguru!",
    "😄 Kalem neden sınavdan kalmış? Çünkü çok yazmış ama hep saçmalamış!",
    "😂 Dondurma neden ağlamış? Çünkü üstüne çikolata dökülmüş!",
    "🤣 Tavuk neden yola çıktı? Diğer tarafa geçmek için!",
    "😜 Saat neden okula geç kalmış? Zamanla yarışamamış!",
    "😆 Kitap neden hastalanmış? Sayfaları dökülüyormuş!",
    "😁 Arı neden matematikten kaldı? Bal yapmayı tercih etmiş!",
    "😅 Fare neden bilgisayarı sevmemiş? Çünkü çok tıklıyormuş!",
    "😛 Karpuz neden futbolcu olamamış? Çünkü çekirdek takımdaymış!",
    "😄 İnternet neden ağlamış? Bağlantısı kesilmiş!",
    "😂 Karınca neden tatile gitmemiş? Formunu kaybetmek istememiş!",
    "🤣 Bilgisayar neden üzgün? Çünkü virüs kapmış!",
    "😜 Otobüs neden mola vermiş? Lastikleri yorulmuş!",
    "😆 Diş fırçası neden gülmüş? Çünkü macun onu gıdıklamış!",
    "😁 Şemsiye neden açılmış? Üzerine çok bastırılmış!",
    "😅 Gitar neden ağlamış? Teli kopmuş!",
    "😛 Ay neden kilo alamamış? Çünkü hep diyetteymiş!",
    "😄 Cüzdan neden boşmuş? Maaş uğramamış!",
    "😂 Müzik neden duraklamış? Ritmini kaybetmiş!",
    "🤣 Öğrenci neden soruyu çözememiş? Çünkü cevap kaçmış!",
    "😜 Havuç neden yürüyememiş? Kök salmış!",
    "🤣 Tavşan neden gözlük takar? Çünkü havuçları yanlış görür!",
    "😂 Limon neden küsmüş? Çünkü suyunu sıkmışlar!",
    "😆 Kitap niye korkmuş? Çünkü kapağını kapatmışlar!",
    "😅 Kurşun kalem neden sevinmiş? Ucu açılmış!",
    "😁 Elma neden sinirliymiş? Sapını çekmişler!",
    "😂 Tost neden konuşamamış? Ağızı peynirliymiş!",
    "😜 Patates neden aynaya bakmış? Cips olmak istemiş!",
    "🤣 Telefon neden ağlamış? Hat çekmemiş!",
    "😄 Ampul neden üzgünmüş? Artık parlak fikirleri yokmuş!",
    "😅 Pizza neden gülmüş? Üstü mantarla doluymuş!",
    "😆 Kalemlik neden sinirlenmiş? Herkes içine giriyormuş!",
    "😂 Priz neden sinirliymiş? Herkes onu fişle tehdit ediyormuş!",
    "🤣 Bulut neden ağlamış? Yağmuru tutamamış!",
    "😁 Gözlük neden düşmüş? Çerçevesi şaşmış!",
    "😄 Asansör neden stresliymiş? Sürekli inip çıkıyormuş!",
    "😜 Radyatör neden yalnızmış? Kimseyle ısınamamış!",
    "😅 Tavuk neden güneşlenmiş? Yumurtası pişsin diye!",
    "😂 Kaşık neden kaçmış? Çünkü çorbayla kavga etmiş!",
    "🤣 Silgi neden işsizmiş? Hata bulamamış!",
    "😄 Çalar saat neden kovulmuş? Hep geç kalıyormuş!",
    "😁 Defter neden sıkılmış? Not alacak konu kalmamış!",
    "😜 Kulaklık neden küsmüş? Müziği dinlememişler!",
    "😆 Ayakkabı neden ağlamış? Bağı çözülmüş!",
    "😅 Kitapçı neden sevinmiş? Çünkü çok satır satmış!",
    "🤣 Laptop neden bozulmuş? Şarjı alınmış!",
    "😂 Çay neden şekersizmiş? Diyetteymiş!",
    "😁 Takvim neden ağlamış? Günü geçmiş!",
    "😜 Harita neden kaybolmuş? Yönünü şaşırmış!"
]

@app.on_message(filters.command("joke") & filters.group & ~BANNED_USERS)
async def random_joke(client, message: Message):
    joke = random.choice(JOKES)
    await message.reply(joke)
