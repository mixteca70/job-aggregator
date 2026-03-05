"""마감일 텍스트 파싱."""

import re
from datetime import datetime


def parse_deadline(text: str) -> str | None:
    """마감일 텍스트를 YYYY-MM-DD 형식으로 반환. 파싱 불가 시 None."""
    if not text or not isinstance(text, str):
        return None
    text = text.strip()
    if not text or text in ("상시", "마감", "-", "—"):
        return None

    # YYYY-MM-DD
    m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if m:
        return f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"

    # YYYY.MM.DD, YYYY/MM/DD
    m = re.search(r"(\d{4})[./](\d{1,2})[./](\d{1,2})", text)
    if m:
        return f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"

    # MM/DD, MM-DD (현재 연도)
    m = re.search(r"(\d{1,2})[/\-](\d{1,2})", text)
    if m:
        y = datetime.now().year
        return f"{y}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"

    # D일 남음
    m = re.search(r"(\d+)\s*일\s*남음", text)
    if m:
        from datetime import timedelta
        d = datetime.now() + timedelta(days=int(m.group(1)))
        return d.strftime("%Y-%m-%d")

    return None
