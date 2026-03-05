"""HTML 제거, 키워드 매칭."""

import re


def clean_html(text: str) -> str:
    """HTML 태그 제거, 공백 정리."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", str(text))
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def match_keywords(text: str, keywords: list[str]) -> list[str]:
    """텍스트에서 매칭된 키워드 목록 반환."""
    if not text or not keywords:
        return []
    text_lower = text.lower()
    return [k for k in keywords if k and k.lower() in text_lower]
