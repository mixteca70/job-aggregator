"""패스트캠퍼스 채용/강사 공고 스크래퍼. 구조 탐색용."""

from urllib.parse import urljoin

from config import KEYWORDS
from scrapers._base import fetch_html, parse_html, sleep_after_request
from utils.date_parser import parse_deadline
from utils.text_cleaner import clean_html, match_keywords

BASE_URL = "https://www.fastcampus.co.kr"
B2B_URL = "https://b2b.fastcampus.co.kr"
SOURCE = "fastcampus"

# 채용 관련 URL 후보 (사이트 구조 변경 시 수정)
CANDIDATE_URLS = [
    f"{B2B_URL}/b2b_instructor_apply",
    f"{BASE_URL}/recruit",
    f"{BASE_URL}/career",
]


def fetch() -> list[dict]:
    """패스트캠퍼스 채용/강사 페이지에서 공고 수집. 구조에 따라 빈 리스트 반환 가능."""
    jobs = []
    seen = set()
    for url in CANDIDATE_URLS:
        html = fetch_html(url)
        if not html:
            continue

        soup = parse_html(html)
        base = url.rsplit("/", 1)[0] if "/" in url else url

        for a in soup.select("a[href]"):
            href = a.get("href", "")
            if not href or href.startswith("javascript:") or href.startswith("#"):
                continue
            link = urljoin(base, href) if not href.startswith("http") else href
            if "fastcampus" not in link:
                continue

            title = clean_html(a.get_text(strip=True))
            if len(title) < 10:
                continue
            if any(skip in title.lower() for skip in ["문의하기", "로그인", "회원가입", "메뉴"]):
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
    return jobs[:50]
