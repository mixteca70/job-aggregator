"""코드잇 채용 공고 스크래퍼. careers.codeit.com."""

from urllib.parse import urljoin

from config import KEYWORDS
from scrapers._base import fetch_html, parse_html, sleep_after_request
from utils.date_parser import parse_deadline
from utils.text_cleaner import clean_html, match_keywords

BASE_URL = "https://careers.codeit.com"
RECRUIT_URL = f"{BASE_URL}/en/recruit"
SOURCE = "codeit"


def fetch() -> list[dict]:
    """코드잇 채용 페이지에서 공고 수집."""
    jobs = []
    html = fetch_html(RECRUIT_URL)
    if not html:
        return []

    soup = parse_html(html)
    seen = set()

    for a in soup.select('a[href*="/en/o/"]'):
        href = a.get("href", "")
        if not href:
            continue
        link = urljoin(BASE_URL, href) if href.startswith("/") else href
        if "codeit.com" not in link or "/en/o/" not in link:
            continue
        if link in seen:
            continue
        seen.add(link)

        title = clean_html(a.get_text(strip=True))
        if len(title) < 3:
            continue
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

    sleep_after_request()
    return jobs
