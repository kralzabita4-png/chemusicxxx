import random
from ArchMusic import userbot
from ArchMusic.core.mongo import mongodb
from ArchMusic.core.userbot import assistants  # Tek seferde import edildi

db = mongodb.assistants

assistantdict = {}  # chat_id -> assistant numarası önbelleği


async def get_client(assistant: int):
    """
    Asistan numarasına göre ilgili userbot client'ını döner.
    """
    if int(assistant) == 1:
        return userbot.one
    elif int(assistant) == 2:
        return userbot.two
    elif int(assistant) == 3:
        return userbot.three
    elif int(assistant) == 4:
        return userbot.four
    elif int(assistant) == 5:
        return userbot.five


async def set_assistant(chat_id):
    """
    Rastgele bir asistan seçer, belleğe ve veritabanına kaydeder.
    Seçilen asistanın userbot client'ını döner.
    """
    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    userbot_client = await get_client(ran_assistant)
    return userbot_client


async def get_assistant(chat_id: int) -> str:
    """
    Verilen chat_id için önce önbellekte asistan aranır.
    Yoksa veritabanından bulunur, yoksa rastgele atanır.
    Userbot client'ı döner.
    """
    assistant = assistantdict.get(chat_id)
    if not assistant:
        try:
            dbassistant = await db.find_one({"chat_id": chat_id})
        except Exception as e:
            print(f"DB hatası: {e}")
            return await set_assistant(chat_id)

        if not dbassistant:
            return await set_assistant(chat_id)
        else:
            got_assis = dbassistant["assistant"]
            if got_assis in assistants:
                assistantdict[chat_id] = got_assis
                return await get_client(got_assis)
            else:
                return await set_assistant(chat_id)
    else:
        if assistant in assistants:
            return await get_client(assistant)
        else:
            return await set_assistant(chat_id)


async def set_calls_assistant(chat_id):
    """
    Rastgele asistan seçer, kaydeder, sadece numarasını döner.
    """
    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    return ran_assistant


async def group_assistant(self, chat_id: int) -> int:
    """
    chat_id için asistan numarasını bulur veya atar,
    self içinden ilgili userbot client'ını döner.
    """
    assistant = assistantdict.get(chat_id)
    if not assistant:
        try:
            dbassistant = await db.find_one({"chat_id": chat_id})
        except Exception as e:
            print(f"DB hatası: {e}")
            assis = await set_calls_assistant(chat_id)
        else:
            if not dbassistant:
                assis = await set_calls_assistant(chat_id)
            else:
                assis = dbassistant["assistant"]
                if assis in assistants:
                    assistantdict[chat_id] = assis
                else:
                    assis = await set_calls_assistant(chat_id)
    else:
        if assistant in assistants:
            assis = assistant
        else:
            assis = await set_calls_assistant(chat_id)

    if int(assis) == 1:
        return self.one
    elif int(assis) == 2:
        return self.two
    elif int(assis) == 3:
        return self.three
    elif int(assis) == 4:
        return self.four
    elif int(assis) == 5:
        return self.five
