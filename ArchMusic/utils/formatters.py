
#

from typing import Union
from pyrogram.types import Message


def get_readable_time(seconds: int) -> str:
    """
    Convert seconds into a human-readable time format.
    Example: 3661 -> "1h:1m:1s"
    """
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]

    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


def convert_bytes(size: float) -> str:
    """
    Convert bytes into human-readable KiB, MiB, GiB, etc.
    Example: 1048576 -> "1.00 MiB"
    """
    if not size:
        return ""
    power = 1024
    t_n = 0
    power_dict = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}

    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])


async def int_to_alpha(user_id: int) -> str:
    """
    Convert integer user_id into alphabet code.
    Example: 123 -> "bcd"
    """
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def alpha_to_int(user_id_alphabet: str) -> int:
    """
    Convert alphabet code back into integer user_id.
    Example: "bcd" -> 123
    """
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    return int(user_id)


def time_to_seconds(time: str) -> int:
    """
    Convert time string "hh:mm:ss" into total seconds.
    Example: "01:02:03" -> 3723
    """
    return sum(
        int(x) * 60**i
        for i, x in enumerate(reversed(str(time).split(":")))
    )


def seconds_to_min(seconds: Union[int, None]) -> str:
    """
    Convert seconds into formatted string dd:hh:mm:ss.
    Example: 3661 -> "01:01:01"
    """
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
        elif h > 0:
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        elif m > 0:
            return "{:02d}:{:02d}".format(m, s)
        elif s > 0:
            return "00:{:02d}".format(s)
    return "-"


formats = [
    "webm", "mkv", "flv", "vob", "ogv", "ogg", "rrc", "gifv", "mng",
    "mov", "avi", "qt", "wmv", "yuv", "rm", "asf", "amv", "mp4", "m4p",
    "m4v", "mpg", "mp2", "mpeg", "mpe", "mpv", "svi", "3gp", "3g2",
    "mxf", "roq", "nsv", "f4v", "f4p", "f4a", "f4b",
]
