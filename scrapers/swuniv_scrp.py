"""SW중심대학 채용·입찰 공고 스크래퍼. MVP - API 불필요."""

import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import KEYWORDS, SWUNIV_URL
from utils.date_parser import parse_deadline
from utils.text_cleaner import clean_html, match_keywords

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BASE_URL = "http://www.swuniv.kr"


def fetch() -> list[dict]:
    """SW중심대학 채용·입찰 페이지에서 공고 수집. jobs 스키마 형식 반환."""
    jobs = []
    try:
        resp = requests.get(
            SWUNIV_URL,
            headers={"User-Agent": USER_AGENT},
            timeout=15,
        )
        resp.encoding = resp.apparent_encoding or "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        # 다양한 선택자 시도 (사이트 구조에 따라 조정)
        for selector in [
            "a[href*='bmode=view']",
            "a[href*='idx=']",
            ".board-list a",
            ".list-item a",
            "table a[href*='/59/']",
        ]:
            for a in soup.select(selector):
                href = a.get("href", "")
                if not href or href.startswith("javascript:"):
                    continue
                title = clean_html(a.get_text(strip=True))
                if len(title) < 5:
                    continue
                link = urljoin(BASE_URL, href) if not href.startswith("http") else href
                if "swuniv.kr" not in link:
                    continue
                matched = match_keywords(title, KEYWORDS)
                jobs.append({
                    "title": title[:200],
                    "link": link,
                    "source": "swuniv",
                    "deadline": parse_deadline(title) or "",
                    "posted_at": "",
                    "description": "",
                    "keywords_matched": ", ".join(matched) if matched else "",
                })
            if jobs:
                break

        # 중복 link 제거
        seen = set()
        unique = []
        for j in jobs:
            if j["link"] not in seen:
                seen.add(j["link"])
                unique.append(j)
        jobs = unique

        time.sleep(2)
    except Exception as e:
        pass  # 실패 시 빈 리스트 반환

    return jobs
