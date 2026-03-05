"""키워드, URL, 설정 상수. Target.md 기반."""

import os
from pathlib import Path

# Target.md 공통 검색 키워드 (8개)
KEYWORDS = [
    "바이브코딩",
    "파이썬 데이터 분석",
    "AI 에이전트",
    "데이터 분석 강사",
    "AI 교육",
    "파이썬 코딩",
    "머신러닝 강사",
    "딥러닝 강사",
]

SARAMIN_API_URL = "https://oapi.saramin.co.kr/job-search"
DB_PATH = str(Path(__file__).parent / "jobs.db")


def get_api_key() -> str | None:
    """사람인 API 키 반환. 환경변수 우선, Streamlit secrets fallback."""
    key = os.environ.get("SARAMIN_ACCESS_KEY")
    if key and key.strip():
        return key.strip()
    try:
        import streamlit as st
        return st.secrets.get("SARAMIN_ACCESS_KEY") or None
    except Exception:
        return None
