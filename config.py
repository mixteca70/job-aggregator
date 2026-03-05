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

DB_PATH = str(Path(__file__).parent / "jobs.db")

# MVP 스크래핑 대상 (API 불필요) - 1차 수집 범위
SWUNIV_URL = "http://www.swuniv.kr/59/"
CODEIT_RECRUIT_URL = "https://careers.codeit.com/en/recruit"
LIKELION_APPLY_URL = "https://likelion.career.greetinghr.com/ko/apply"
MODULABS_APPLY_URL = "https://modulabs.career.greetinghr.com/en/apply"
FASTCAMPUS_B2B_URL = "https://b2b.fastcampus.co.kr/b2b_instructor_apply"
ELICE_JOBS_URL = "https://elice.careers/jobs"
CAREERLY_URL = "https://careerly.co.kr"

# Phase 2 API (승인 후 사용)
SARAMIN_API_URL = "https://oapi.saramin.co.kr/job-search"


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
