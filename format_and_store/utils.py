from typing import Optional
from datetime import datetime

def parse_date_or_none(date_str: Optional[str]) -> Optional[str]:
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None

def str_to_list(s):
    if not s:
        return []
    return [item.strip() for item in s.split(",") if item.strip()]
