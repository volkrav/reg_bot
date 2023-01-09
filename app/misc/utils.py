import datetime

import pytz


TZ = pytz.timezone("Europe/Kiev")

def get_now_datetime() -> datetime.datetime:
    now = datetime.datetime.now(TZ)
    return now


def get_now_formatted(dt: datetime.datetime = None) -> str:
    if not dt:
        dt = get_now_datetime()
    return dt.strftime("%H:%M:%S %d-%m-%Y")


def is_day() -> bool:
    return 7 < datetime.datetime.now(TZ).hour < 24
