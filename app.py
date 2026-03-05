"""Streamlit 메인 진입점. MVP 완성."""

import streamlit as st
import pandas as pd

from config import KEYWORDS
from database.db_handler import init_db, insert_job, get_jobs, insert_sample_jobs
from scrapers.registry import fetch_all
from utils.deduplicator import deduplicate_by_link

SOURCES = ["swuniv", "codeit", "likelion", "modulabs", "fastcampus", "elice", "careerly"]

st.set_page_config(page_title="AI 강사 채용 공고", layout="wide")
st.title("AI/Data Instructor Job Aggregator")

# 초기화
if "init_done" not in st.session_state:
    init_db()
    st.session_state.init_done = True

# 사이드바
with st.sidebar:
    st.subheader("필터")
    keyword_filter = st.multiselect("키워드", KEYWORDS, default=[])
    source_filter = st.selectbox("소스", ["전체"] + SOURCES, index=0)
    sort_filter = st.selectbox("정렬", ["마감일 오름차순", "마감일 내림차순", "최신순"], index=0)

    st.divider()
    if st.button("공고 수집"):
        with st.spinner("수집 중..."):
            jobs = fetch_all()
            jobs = deduplicate_by_link(jobs)
            for j in jobs:
                insert_job(j)
            st.success(f"{len(jobs)}건 수집 완료")
            st.rerun()

    if st.button("샘플 데이터 로드"):
        n = insert_sample_jobs()
        st.success(f"샘플 {n}건 로드")
        st.rerun()

# 필터 적용
filters = {}
if keyword_filter:
    filters["keyword"] = " ".join(keyword_filter)
if source_filter != "전체":
    filters["source"] = source_filter
sort_map = {"마감일 오름차순": "deadline_asc", "마감일 내림차순": "deadline_desc", "최신순": "created_at"}
filters["sort"] = sort_map.get(sort_filter, "deadline_asc")

rows = get_jobs(filters)
if rows:
    df = pd.DataFrame(rows)
    display_cols = ["title", "source", "deadline", "keywords_matched", "link"]
    df_display = df[[c for c in display_cols if c in df.columns]]
    st.dataframe(df_display, use_container_width=True, column_config={"link": st.column_config.LinkColumn("링크")})
else:
    st.info("공고가 없습니다. '공고 수집' 또는 '샘플 데이터 로드'를 클릭하세요.")
