# AI/Data Instructor Job Aggregator & Scheduler

웹에서 데이터 분석, 머신러닝, 딥러닝 강사 및 교육 공고를 수집하고 지원 일정을 관리하는 Streamlit 기반 웹앱입니다.

---

## 빠른 시작

```bash
git clone https://github.com/YOUR_USERNAME/job-aggregator.git
cd job-aggregator
pip install -r requirements.txt
streamlit run app.py
```

**가상환경 (권장):** `python -m venv venv` → Windows: `.\venv\Scripts\Activate.ps1` / Linux: `source venv/bin/activate`

---

## 구축 단계

| Phase | 수집 방식 | 대상 | API 키 |
|-------|------------|------|--------|
| **MVP** | 스크래핑 | SW중심대학, 패스트캠퍼스, 멋사 | 불필요 |
| **Phase 2** | API | 사람인, 원티드, 워크넷, 나라장터 | 필요 |

---

## 구현 순서 (MVP)

| 단계 | 작업 | 상태 |
|------|------|------|
| 0 | 프로젝트 초기화 | 완료 |
| 1 | config.py | 완료 |
| 2 | db_handler.py | |
| 3 | utils (date_parser, deduplicator, text_cleaner) | |
| 4 | swuniv_scrp.py | |
| 5 | app.py | |

**데이터 흐름:** SW중심대학 HTML → swuniv_scrp.fetch() → deduplicate_by_link → insert_job → get_jobs → st.dataframe

**단계별 상세:**
- 단계 2: `get_jobs(filters)` — keyword, source, sort(deadline asc/desc)
- 단계 4: 대상 `http://www.swuniv.kr/59/`, BeautifulSoup+requests, User-Agent, 요청 간격 2초
- job dict: `{title, link, source, deadline, posted_at, description, keywords_matched}`

**샘플 job (테스트용):**
```python
{"title": "[강사] 파이썬 데이터 분석", "link": "https://example.com/1", "source": "swuniv",
 "deadline": "2025-04-15", "posted_at": "2025-03-01", "description": "", "keywords_matched": "파이썬"}
```

**검증 명령:**
- 1: `python -c "from config import KEYWORDS; assert len(KEYWORDS) >= 6"`
- 2: `python -c "from database.db_handler import init_db, insert_job, get_jobs; init_db(); insert_job({'title':'t','link':'https://x.com/1','source':'swuniv','deadline':'2025-04-01','posted_at':'','description':'','keywords_matched':''}); print(len(get_jobs()))"`
- 3: `python -c "from utils.date_parser import parse_deadline; from utils.deduplicator import deduplicate_by_link; assert parse_deadline('2025-03-31'); assert len(deduplicate_by_link([{'link':'a'},{'link':'a'}]))==1"`
- 4: `python -c "from scrapers.swuniv_scrp import fetch; print('OK:', len(fetch()))"`
- 5: `streamlit run app.py` → 수집 → 목록 표시

**Phase 2:** API 키 승인 시 saramin_scrp 등 추가. 환경변수: SARAMIN_ACCESS_KEY, WANTED_CLIENT_ID/SECRET, WORKNET_API_KEY, DATA_GO_KR_SERVICE_KEY. 로컬: `copy .streamlit\secrets.toml.example .streamlit\secrets.toml` 후 입력. Streamlit Cloud: 앱 설정 → Secrets 탭.

---

## 주요 기능

1. **Multi-Source Scraping**: [Target.md](Target.md) 정의 사이트에서 공고 수집
2. **Keyword Filtering**: 바이브코딩, 파이썬 데이터 분석, AI 에이전트 등
3. **Smart Scheduling**: 마감일 추출 → 캘린더/목록 표시
4. **Duplicate Handling**: link 기준 중복 제거

---

## 기술 스택

Python 3.10+, Streamlit, BeautifulSoup4, requests, SQLite, Pandas

**requirements.txt:** streamlit, pandas, requests, beautifulsoup4, lxml

---

## 프로젝트 구조

```text
.
├── app.py, config.py, requirements.txt
├── .streamlit/config.toml, secrets.toml.example
├── scrapers/ (swuniv_scrp.py 등)
├── database/ (db_handler.py, schema.sql)
└── utils/ (date_parser, deduplicator, text_cleaner)
```

---

## 데이터베이스

**jobs:** id, title, link(UNIQUE), source, deadline, posted_at, description, keywords_matched, created_at

**scrape_logs (선택):** id, source, status, message, created_at

---

## 배포

1. [share.streamlit.io](https://share.streamlit.io) → GitHub 로그인
2. New app → Repository, Branch(main), Main file(app.py) 선택
3. Phase 2 API 시: Secrets 탭에 `SARAMIN_ACCESS_KEY = "키"` 입력

---

## 스크래핑·DB 주의사항

- 요청 간격 2초 이상, User-Agent 설정, robots.txt 준수
- 중복: link 기준, URL 정규화(utm_ 등 제거), INSERT OR REPLACE 또는 ON CONFLICT

---

## 트러블슈팅

| 증상 | 해결 |
|------|------|
| 403 Forbidden | User-Agent: Mozilla/5.0 설정 |
| 빈 리스트 | HTML 구조 변경 → CSS 선택자 수정 |
| Connection timeout | 요청 간격 2초, 재시도 |
| DB locked | Streamlit 종료 후 재시도 |
| ModuleNotFoundError | 프로젝트 루트 실행, __init__.py 확인 |
| no such table: jobs | init_db() 먼저 호출 |
| UNIQUE constraint (link) | ON CONFLICT 또는 INSERT OR REPLACE |
| API 401 (Phase 2) | SARAMIN_ACCESS_KEY 환경변수 또는 secrets.toml |
| 포트 8501 사용 중 | Ctrl+C 후 streamlit run 재실행 |

---

## 협업

- 브랜치: main(배포), feature/xxx(기능)
- PR 전: 위 검증 명령 통과, API 키 코드 미포함

---

## 참고

- [Target.md](Target.md): 수집 대상 사이트, 키워드, API/스크래핑 방법 상세
- [사람인 API](https://oapi.saramin.co.kr), [원티드 OpenAPI](https://openapi.wanted.jobs), [고용24](https://www.work24.go.kr), [공공데이터포털](https://www.data.go.kr)
