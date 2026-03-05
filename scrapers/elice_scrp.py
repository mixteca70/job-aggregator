"""엘리스 채용 공고 스크래퍼. elice.careers."""

from urllib.parse import urljoin

from config import KEYWORDS
from scrapers._base import fetch_html, parse_html, sleep_after_request
from utils.date_parser import parse_deadline
from utils.text_cleaner import clean_html, match_keywords

BASE_URL = "https://elice.careers"
JOBS_URL = f"{BASE_URL}/jobs"
SOURCE = "elice"


def fetch() -> list[dict]:
    """엘리스 채용 페이지에서 공고 수집. JS 렌더링 시 빈 리스트 가능."""
    jobs = []
    html = fetch_html(JOBS_URL)
    if not html:
        return []

    soup = parse_html(html)
    seen = set()

    for a in soup.select("a[href]"):
        href = a.get("href", "")
        if not href or href.startswith("javascript:") or href.startswith("#"):
            continue
        link = urljoin(BASE_URL, href) if not href.startswith("http") else href
        if "elice" not in link:
            continue

        title = clean_html(a.get_text(strip=True))
        if len(title) < 5:
            continue
        if any(skip in title for skip in ["×", "원문 보기", "지금 주목할"]):
            continue
        title = title[:200]

        if link in seen:
            continue
        seen.add(link)

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

    sleep_after_request()
    return jobs
