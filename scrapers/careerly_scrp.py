"""커리어리 채용 공고 스크래퍼. 채용 섹션 탐색용."""

from urllib.parse import urljoin

from config import KEYWORDS
from scrapers._base import fetch_html, parse_html, sleep_after_request
from utils.date_parser import parse_deadline
from utils.text_cleaner import clean_html, match_keywords

BASE_URL = "https://careerly.co.kr"
SOURCE = "careerly"

CANDIDATE_URLS = [
    f"{BASE_URL}/",
    f"{BASE_URL}/jobs",
    f"{BASE_URL}/recruit",
]


def fetch() -> list[dict]:
    """커리어리 채용 페이지에서 공고 수집. 전용 채용 페이지 미확인 시 빈 리스트."""
    jobs = []
    seen = set()
    for url in CANDIDATE_URLS:
        html = fetch_html(url)
        if not html:
            continue

        soup = parse_html(html)
        base = url.rsplit("/", 1)[0] if "/" in url.rstrip("/") else url

        for a in soup.select("a[href*='careerly']"):
            href = a.get("href", "")
            if not href or href.startswith("javascript:"):
                continue
            link = urljoin(base, href) if not href.startswith("http") else href
            if "careerly" not in link:
                continue

            title = clean_html(a.get_text(strip=True))
            if len(title) < 8:
                continue
            if any(skip in title for skip in ["로그인", "회원가입", "Q&A", "트렌드"]):
                continue
            if link in seen:
                continue
            seen.add(link)
            title = title[:200]

            matched = match_keywords(title, KEYWORDS)
            jobs.append({
                "title": title,
                "link": link,
                "source": SOURCE,
                "deadline": parse_deadline(title) or "",
                "posted_at": "",
                "description": "",
                "keywords_matched": ", ".join(matched) if matched else "",
            })

        if jobs:
            break
        sleep_after_request()

    sleep_after_request()
    return jobs[:30]
