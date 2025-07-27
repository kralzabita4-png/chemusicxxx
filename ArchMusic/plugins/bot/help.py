# Copyright (C) 2021-2023 by ArchBots@Github, < https://github.com/ArchBots >
# This file is part of < https://github.com/ArchBots/ArchMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/ArchBots/ArchMusic/blob/master/LICENSE >

from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from config import BANNED_USERS
from strings import get_command, get_string, helpers
from ArchMusic import app
from ArchMusic.misc import SUDOERS
from ArchMusic.utils import help_pannel
from ArchMusic.utils.database import get_lang, is_commanddelete_on
from ArchMusic.utils.decorato
