from datetime import datetime, timedelta, timezone
import re

TIME_INTERVAL_PATTERN = r"^(\d+)([hdwm])$"
TIME_PATTERN = r"^(\w\w\w \d\d?, \d\d\d\d)\W+(\d\d?:\d\d [AP]M UTC)$"

TIME_INTERVAL_BEFORE : dict[int, datetime] = {
    "h": (lambda x : datetime.now(timezone.utc) - timedelta(hours=x)),
    "d": (lambda x : datetime.now(timezone.utc) - timedelta(days=x)),
    "w": (lambda x : datetime.now(timezone.utc) - timedelta(weeks=x)),
    "m": (lambda x : datetime.now(timezone.utc) - timedelta(days=30*x)),
}

def time_before(time_interval_str: str) -> datetime:
    res = re.search(TIME_INTERVAL_PATTERN, time_interval_str)
    return TIME_INTERVAL_BEFORE[res.group(2)](int(res.group(1)))

def get_datetime(time_string: str) -> datetime:
    res = re.search(TIME_PATTERN, time_string)
    return datetime.strptime(res.group(1) + ' ' + res.group(2), '%b %d, %Y %I:%M %p UTC').replace(tzinfo=timezone.utc)
