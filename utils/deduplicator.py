"""Link 기준 중복 제거."""

import re
from urllib.parse import urlparse, urlunparse


def _normalize_link(link: str) -> str:
    """URL 정규화: utm_, ref 등 쿼리 제거."""
    if not link:
        return ""
    try:
        parsed = urlparse(link)
        query_parts = []
        if parsed.query:
            for p in parsed.query.split("&"):
                if "=" in p:
                    k, _ = p.split("=", 1)
                    if not re.match(r"utm_|ref|fbclid", k.lower()):
                        query_parts.append(p)
        new_query = "&".join(query_parts) if query_parts else ""
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    except Exception:
        return link


def deduplicate_by_link(jobs: list[dict]) -> list[dict]:
    """link 기준 중복 제거. 먼저 나온 항목 유지."""
    seen = set()
    result = []
    for j in jobs:
        link = j.get("link", "")
        norm = _normalize_link(link)
        if norm and norm not in seen:
            seen.add(norm)
            result.append(j)
    return result
