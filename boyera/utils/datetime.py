from typing import Optional

from datetime import timedelta
from datetime import datetime
from zoneinfo import ZoneInfo

jktZone = ZoneInfo("Asia/Jakarta")

def getCurrentTime() -> datetime:
    return datetime.now(tz=jktZone)

def addTimeBySeconds(seconds: str, currentDate: Optional[datetime] = None) -> datetime:
    if not currentDate:
        currentDate = getCurrentTime()

    date = currentDate + timedelta(seconds=seconds)

    return date
