import math
import json
from pyrogram.types import InlineKeyboardButton
from ArchMusic.utils.formatters import time_to_seconds


# ——— Progress Bar ———
def get_progress_bar(percentage: float, length: int = 15) -> str:
    filled_length = int(length * percentage // 100)
    bar = "█" * filled_length + "░" * (length - filled_length)
    return f"{bar} {percentage:.0f}%"


# ——— Callback Data JSON Formatı ———
def make_callback(action: str, chat_id: int, extra: dict = None) -> str:
    data = {"action": action, "chat_id": chat_id}
    if extra:
        data.update(extra)
    return json.dumps(data)


# ——— Buton Oluşturucu ———
def create_buttons(buttons_config: list, chat_id: int):
    buttons = []
    for btn in buttons_config:
        buttons.append(
            InlineKeyboardButton(
                text=btn["text"],
                callback_data=make_callback(btn["action"], chat_id, btn.get("extra"))
            )
        )
    return buttons


# ——— Stream Kontrolleri ———
def stream_controls(chat_id: int):
    config = [
        {"text": "▶️ Başla", "action": "Resume"},
        {"text": "⏸ Duraklat", "action": "Pause"},
        {"text": "⏭ Atlama", "action": "Skip"},
        {"text": "🟥 Bitir", "action": "Stop"},
    ]
    return create_buttons(config, chat_id)


# ——— Stream Markup (Zaman Çubuğu Dahil) ———
def stream_markup_timer(_, videoid, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100 if duration_sec else 0

    progress_bar = get_progress_bar(percentage)

    buttons = [
        [InlineKeyboardButton(text=f"{played} {progress_bar} {dur}", callback_data="GetTimer")],
        [InlineKeyboardButton(text="🏃‍♂️ Sürekli Oynat", callback_data=make_callback("Loop", chat_id))],
        [
            InlineKeyboardButton(text="⏪ -10s", callback_data=make_callback("JumpBack10", chat_id)),
            InlineKeyboardButton(text="⏩ +10s", callback_data=make_callback("JumpForward10", chat_id)),
            InlineKeyboardButton(text="⏪ -30s", callback_data=make_callback("JumpBack30", chat_id)),
            InlineKeyboardButton(text="⏩ +30s", callback_data=make_callback("JumpForward30", chat_id)),
        ],
        stream_controls(chat_id),
        [InlineKeyboardButton(text="❌ Menüyü Kapat", callback_data="close")],
    ]
    return buttons


# ——— Stream Markup (Zaman Çubuğu Olmadan) ———
def stream_markup(_, videoid, chat_id):
    buttons = [
        [InlineKeyboardButton(text="🏃‍♂️ Sürekli Oynat", callback_data=make_callback("Loop", chat_id))],
        [
            InlineKeyboardButton(text="⏪ -10s", callback_data=make_callback("JumpBack10", chat_id)),
            InlineKeyboardButton(text="⏩ +10s", callback_data=make_callback("JumpForward10", chat_id)),
            InlineKeyboardButton(text="⏪ -30s", callback_data=make_callback("JumpBack30", chat_id)),
            InlineKeyboardButton(text="⏩ +30s", callback_data=make_callback("JumpForward30", chat_id)),
        ],
        stream_controls(chat_id),
        [InlineKeyboardButton(text="❌ Menüyü Kapat", callback_data="close")],
    ]
    return buttons


# ——— Telegram Markup Timer ———
def telegram_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100 if duration_sec else 0

    progress_bar = get_progress_bar(percentage)

    buttons = [
        [InlineKeyboardButton(text=f"{played} {progress_bar} {dur}", callback_data="GetTimer")],
        [InlineKeyboardButton(text=_["PL_B_3"], callback_data=make_callback("PanelMarkupNone", chat_id))],
        [
            InlineKeyboardButton(text="▷", callback_data=make_callback("Resume", chat_id)),
            InlineKeyboardButton(text="II", callback_data=make_callback("Pause", chat_id)),
            InlineKeyboardButton(text="‣‣I", callback_data=make_callback("Skip", chat_id)),
            InlineKeyboardButton(text="▢", callback_data=make_callback("Stop", chat_id)),
        ],
        [InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close")],
    ]
    return buttons


# ——— Telegram Markup ———
def telegram_markup(_, chat_id):
    buttons = [
        [InlineKeyboardButton(text=_["PL_B_3"], callback_data=make_callback("PanelMarkupNone", chat_id))],
        [
            InlineKeyboardButton(text="▷", callback_data=make_callback("Resume", chat_id)),
            InlineKeyboardButton(text="II", callback_data=make_callback("Pause", chat_id)),
            InlineKeyboardButton(text="‣‣I", callback_data=make_callback("Skip", chat_id)),
            InlineKeyboardButton(text="▢", callback_data=make_callback("Stop", chat_id)),
        ],
        [InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close")],
    ]
    return buttons


# ——— Track Markup ———
def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_1"], callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["P_B_2"], callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}")
        ],
    ]
    return buttons


# ——— Playlist Markup ———
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_1"], callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["P_B_2"], callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}"),
        ],
    ]
    return buttons


# ——— Livestream Markup ———
def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_3"], callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}"),
        ],
    ]
    return buttons


# ——— Slider Markup ———
def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query_short = query[:20]
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_1"], callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["P_B_2"], callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"),
        ],
        [
            InlineKeyboardButton(text="❮", callback_data=f"slider B|{query_type}|{query_short}|{user_id}|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {query_short}|{user_id}"),
            InlineKeyboardButton(text="❯", callback_data=f"slider F|{query_type}|{query_short}|{user_id}|{channel}|{fplay}"),
        ],
    ]
    return buttons


# ——— Panel Markup 1 ———
def panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="⏸ Pause", callback_data=make_callback("Pause", chat_id)),
            InlineKeyboardButton(text="▶️ Resume", callback_data=make_callback("Resume", chat_id)),
        ],
        [
            InlineKeyboardButton(text="⏯ Skip", callback_data=make_callback("Skip", chat_id)),
            InlineKeyboardButton(text="⏹ Stop", callback_data=make_callback("Stop", chat_id)),
        ],
        [
            InlineKeyboardButton(text="🔁 Replay", callback_data=make_callback("Replay", chat_id)),
        ],
        [
            InlineKeyboardButton(text="◀️", callback_data=make_callback("PagesBack", chat_id, {"page": 0, "videoid": videoid})),
            InlineKeyboardButton(text="🔙 Back", callback_data=make_callback("MainMarkup", chat_id, {"videoid": videoid})),
            InlineKeyboardButton(text="▶️", callback_data=make_callback("PagesForw", chat_id, {"page": 0, "videoid": videoid})),
        ],
    ]
    return buttons


# ——— Panel Markup 2 ———
def panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="🔇 Mute", callback_data=make_callback("Mute", chat_id)),
            InlineKeyboardButton(text="🔊 Unmute", callback_data=make_callback("Unmute", chat_id)),
        ],
        [
            InlineKeyboardButton(text="🔀 Shuffle", callback_data=make_callback("Shuffle", chat_id)),
            InlineKeyboardButton(text="🔁 Loop", callback_data=make_callback("Loop", chat_id)),
        ],
        [
            InlineKeyboardButton(text="◀️", callback_data=make_callback("PagesBack", chat_id, {"page": 1, "videoid": videoid})),
            InlineKeyboardButton(text="🔙 Back", callback_data=make_callback("MainMarkup", chat_id, {"videoid": videoid})),
            InlineKeyboardButton(text="▶️", callback_data=make_callback("PagesForw", chat_id, {"page": 1, "videoid": videoid})),
        ],
    ]
    return buttons


# ——— Panel Markup 3 ———
def panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="⏮ 10 seconds", callback_data=make_callback("JumpBack10", chat_id)),
            InlineKeyboardButton(text="⏭ 10 seconds", callback_data=make_callback("JumpForward10", chat_id)),
        ],
        [
            InlineKeyboardButton(text="⏮ 30 seconds", callback_data=make_callback("JumpBack30", chat_id)),
            InlineKeyboardButton(text="⏭ 30 seconds", callback_data=make_callback("JumpForward30", chat_id)),
        ],
        [
            InlineKeyboardButton(text="◀️", callback_data=make_callback("PagesBack", chat_id, {"page": 2, "videoid": videoid})),
            InlineKeyboardButton(text="🔙 Back", callback_data=make_callback("MainMarkup", chat_id, {"videoid": videoid})),
            InlineKeyboardButton(text="▶️", callback_data=make_callback("PagesForw", chat_id, {"page": 2, "videoid": videoid})),
        ],
    ]
    return buttons
