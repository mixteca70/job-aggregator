"""DB 연결, 초기화, CRUD."""

import sqlite3
from pathlib import Path

from config import DB_PATH

_SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    try:
        conn.executescript(_SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()


def insert_job(job: dict) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO jobs (title, link, source, deadline, posted_at, description, keywords_matched)
            VALUES (:title, :link, :source, :deadline, :posted_at, :description, :keywords_matched)
            ON CONFLICT(link) DO UPDATE SET
                title=excluded.title, deadline=excluded.deadline, posted_at=excluded.posted_at,
                description=excluded.description, keywords_matched=excluded.keywords_matched
            """,
            {
                "title": job.get("title", ""),
                "link": job.get("link", ""),
                "source": job.get("source", ""),
                "deadline": job.get("deadline") or "",
                "posted_at": job.get("posted_at") or "",
                "description": job.get("description") or "",
                "keywords_matched": job.get("keywords_matched") or "",
            },
        )
        conn.commit()
    finally:
        conn.close()


def get_jobs(filters: dict | None = None) -> list[dict]:
    filters = filters or {}
    keyword = filters.get("keyword")
    source = filters.get("source")
    sort = filters.get("sort", "deadline_asc")

    conn = get_connection()
    try:
        where_parts = []
        params = []
        if keyword:
            terms = [t.strip() for t in str(keyword).split() if t.strip()]
            if terms:
                conds = []
                for t in terms:
                    conds.append("(title LIKE ? OR keywords_matched LIKE ?)")
                    params.extend([f"%{t}%", f"%{t}%"])
                where_parts.append("(" + " OR ".join(conds) + ")")
        if source:
            where_parts.append("source = ?")
            params.append(source)

        where_sql = " AND ".join(where_parts) if where_parts else "1=1"
        if sort == "deadline_asc":
            order = "deadline ASC"
        elif sort == "deadline_desc":
            order = "deadline DESC"
        else:
            order = "created_at DESC"

        rows = conn.execute(
            f"SELECT id, title, link, source, deadline, posted_at, description, keywords_matched, created_at "
            f"FROM jobs WHERE {where_sql} ORDER BY {order}",
            params,
        ).fetchall()

        return [
            {
                "id": r[0],
                "title": r[1],
                "link": r[2],
                "source": r[3],
                "deadline": r[4],
                "posted_at": r[5],
                "description": r[6],
                "keywords_matched": r[7],
                "created_at": r[8],
            }
            for r in rows
        ]
    finally:
        conn.close()


def insert_sample_jobs() -> int:
    """UI 테스트용 샘플 1차 수집 소스별 삽입. 반환: 삽입 건수."""
    samples = [
        {"title": "[강사] 파이썬 데이터 분석", "link": "https://example.com/sample1", "source": "swuniv",
         "deadline": "2025-04-15", "posted_at": "2025-03-01", "description": "", "keywords_matched": "파이썬, 데이터 분석"},
        {"title": "[강사] AI 에이전트 교육", "link": "https://example.com/sample2", "source": "swuniv",
         "deadline": "2025-04-30", "posted_at": "2025-03-02", "description": "", "keywords_matched": "AI 에이전트"},
        {"title": "데이터 분석가 부트캠프 강사", "link": "https://careers.codeit.com/en/o/174500", "source": "codeit",
         "deadline": "", "posted_at": "", "description": "", "keywords_matched": "데이터 분석 강사"},
        {"title": "AI 엔지니어 부트캠프 강사", "link": "https://careers.codeit.com/en/o/174374", "source": "codeit",
         "deadline": "", "posted_at": "", "description": "", "keywords_matched": "AI 교육"},
        {"title": "[AI 교육 신사업] 사업개발 매니저", "link": "https://likelion.career.greetinghr.com/ko/o/203338", "source": "likelion",
         "deadline": "", "posted_at": "", "description": "", "keywords_matched": "AI 교육"},
        {"title": "[KDT사업] 부트캠프 교육 수강 문의", "link": "https://modulabs.career.greetinghr.com/en/o/203615", "source": "modulabs",
         "deadline": "", "posted_at": "", "description": "", "keywords_matched": ""},
    ]
    for j in samples:
        insert_job(j)
    return len(samples)
