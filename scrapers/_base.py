"""스크래퍼 공통 설정 및 헬퍼."""

import time

import requests
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
REQUEST_DELAY = 2


def fetch_html(url: str, timeout: int = 15) -> str | None:
    """URL에서 HTML 텍스트 반환. 실패 시 None."""
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
        )
        resp.encoding = resp.apparent_encoding or "utf-8"
        return resp.text
    except Exception:
        return None


def parse_html(html: str) -> BeautifulSoup:
    """HTML 문자열을 BeautifulSoup 객체로 변환."""
    return BeautifulSoup(html, "html.parser")


def sleep_after_request():
    """요청 간격 준수."""
    time.sleep(REQUEST_DELAY)
