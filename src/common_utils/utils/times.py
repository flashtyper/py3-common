from datetime import datetime

def format_date(ts: datetime) -> str:
    # Returns string from given datetime object in format `01.12.2026-04:12:12`
    return ts.strftime("%d.%m.%Y-%H:%M:%S")

