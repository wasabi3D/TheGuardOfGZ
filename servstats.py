import os
import pickle
import time
from datetime import datetime
from typing import Optional
from enum import Enum
import discord


class StatType(Enum):
    MSGNUM = 1
    VOCALTIME = 2


ACTIVITY_PATH = "data/stats/activity"
if not os.path.exists(ACTIVITY_PATH):
    os.makedirs(ACTIVITY_PATH)


def toID(year: int, week: int):
    return f"{year}-{week}"


def getCurrentWeekID():
    unix = time.time()
    date = datetime.utcfromtimestamp(unix)
    iso = date.isocalendar()
    return toID(iso[0], iso[1])


def getPath(week_id: str) -> str:
    return f"{ACTIVITY_PATH}/{week_id}.dat"


SAVE_MIN_INTERVAL = 60
last_saved = time.time()

empty = {StatType.MSGNUM: 0, StatType.VOCALTIME: 0}
# 1st key: user id, 2nd key: messages or vocaltime
current_stats: dict[int, dict[StatType, int]] = {}
current_week_id = getCurrentWeekID()

target_file_path = getPath(current_week_id)
if os.path.exists(target_file_path):
    with open(target_file_path, "rb") as f:
        current_stats = pickle.load(f)


def checkWeekID():
    global current_week_id, current_stats
    if getCurrentWeekID() == current_week_id:
        return
    save(force=True)
    current_week_id = getCurrentWeekID()
    current_stats = {}
    return


def save(force=False):
    global last_saved
    if time.time() - last_saved < SAVE_MIN_INTERVAL or force:
        return

    with open(target_file_path, "wb") as f:
        pickle.dump(current_stats, f)

    last_saved = time.time()
    return


def onMessage(message: discord.Message):
    user_id = message.author.id
    if user_id not in current_stats:
        current_stats[user_id] = empty.copy()
    checkWeekID()
    current_stats[user_id][StatType.MSGNUM] += 1
    save()
    return


def getStats(year: int, week: int) -> Optional[dict[int, dict[StatType, int]]]:
    week_id = toID(year, week)
    if week_id == current_week_id:
        return current_stats

    archive_path = getPath(week_id)
    if not os.path.exists(archive_path):
        return None

    with open(archive_path, "rb") as f:
        return pickle.load(f)
