from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from ArchMusic import app

# 🎲 /dice - Zar atar
@app.on_message(filters.command("dice") & filters.group & ~BANNED_USERS)
async def at_dice(client, message: Message):
    await message.reply_dice(emoji="🎲")

# 🎯 /dart - Dart oku atar
@app.on_message(filters.command("dart") & filters.group & ~BANNED_USERS)
async def at_dart(client, message: Message):
    await message.reply_dice(emoji="🎯")

# 🏀 /ball - Basketbol atışı yapar
@app.on_message(filters.command("ball") & filters.group & ~BANNED_USERS)
async def at_ball(client, message: Message):
    await message.reply_dice(emoji="🏀")

# ⚽ /goal - Futbol topu atar
@app.on_message(filters.command("goal") & filters.group & ~BANNED_USERS)
async def at_goal(client, message: Message):
    await message.reply_dice(emoji="⚽")

# 🎰 /slot - Slot makinesi çevirir
@app.on_message(filters.command("slot") & filters.group & ~BANNED_USERS)
async def at_slot(client, message: Message):
    await message.reply_dice(emoji="🎰")

# 🎳 /bowling - Bowling topu atar
@app.on_message(filters.command("bowling") & filters.group & ~BANNED_USERS)
async def at_bowling(client, message: Message):
    await message.reply_dice(emoji="🎳")
