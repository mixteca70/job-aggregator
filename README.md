# AI/Data Instructor Job Aggregator & Scheduler

웹에서 데이터 분석, 머신러닝, 딥러닝 강사 및 교육 공고를 수집하고 지원 일정을 관리하는 Streamlit 기반 웹앱입니다.

---

## 빠른 시작

```bash
git clone https://github.com/mixteca70/job-aggregator.git
cd job-aggregator
pip install -r requirements.txt
streamlit run app.py
```

**가상환경 (권장):** `python -m venv venv` → Windows: `.\venv\Scripts\Activate.ps1` / Linux: `source venv/bin/activate`

---

## 구현 현황

| Phase | 수집 방식 | 구현 대상 | API 키 |
|-------|------------|-----------|--------|
| **MVP (1차 수집)** | 스크래핑 | SW중심대학, 코드잇, 멋사, 모두의연구소, 패스트캠퍼스, 엘리스, 커리어리 | 불필요 |
| **Phase 2** | API | 사람인, 원티드, 워크넷, 나라장터 | 필요 |

---

## 구현 내용 (모듈별)

### config.py
- `KEYWORDS`: 8개 (바이브코딩, 파이썬 데이터 분석, AI 에이전트, 데이터 분석 강사, AI 교육, 파이썬 코딩, 머신러닝 강사, 딥러닝 강사)
- `DB_PATH`: 프로젝트 루트 `jobs.db`
- 1차 수집 URL: SWUNIV_URL, CODEIT_RECRUIT_URL, LIKELION_APPLY_URL, MODULABS_APPLY_URL, FASTCAMPUS_B2B_URL, ELICE_JOBS_URL, CAREERLY_URL
- `get_api_key()`: Phase 2용, 환경변수 `SARAMIN_ACCESS_KEY` 또는 Streamlit secrets

### database/db_handler.py
- `init_db()`: schema.sql 실행, jobs·scrape_logs 테이블 생성
- `insert_job(job)`: ON CONFLICT(link) DO UPDATE로 중복 시 갱신
- `get_jobs(filters)`: keyword(OR 검색), source, sort(deadline_asc/desc, created_at)
- `insert_sample_jobs()`: 테스트용 6건 삽입 (소스별)

### utils/
| 모듈 | 함수 | 역할 |
|------|------|------|
| date_parser | `parse_deadline(text)` | YYYY-MM-DD, YYYY.MM.DD, MM/DD, D일 남음 → 표준 형식, 상시/마감 시 None |
| deduplicator | `deduplicate_by_link(jobs)` | link 기준 중복 제거, `_normalize_link`로 utm_/ref/fbclid 제거 |
| text_cleaner | `clean_html(text)`, `match_keywords(text, keywords)` | HTML 제거, 키워드 매칭 |

### scrapers/ (1차 수집 범위)
| 모듈 | 대상 | URL | 비고 |
|------|------|-----|------|
| swuniv_scrp | SW중심대학 | swuniv.kr/59/ | 채용·입찰 |
| codeit_scrp | 코드잇 | careers.codeit.com/en/recruit | Wantedly 스타일 |
| likelion_scrp | 멋쟁이사자처럼 | likelion.career.greetinghr.com/ko/apply | GreetingHR |
| modulabs_scrp | 모두의연구소 | modulabs.career.greetinghr.com/en/apply | GreetingHR |
| fastcampus_scrp | 패스트캠퍼스 | b2b.fastcampus.co.kr | 구조 탐색용 |
| elice_scrp | 엘리스 | elice.careers/jobs | JS 렌더링 시 빈 리스트 가능 |
| careerly_scrp | 커리어리 | careerly.co.kr | 전용 채용 페이지 미확인 |
| `_base.py` | 공통 | `fetch_html`, `parse_html`, `sleep_after_request` | |
| `registry.py` | 통합 | `fetch_all()` | 7개 소스 순차 수집 |

### app.py
- 사이드바: 키워드(multiselect), 소스(전체/swuniv/codeit/likelion/modulabs/fastcampus/elice/careerly), 정렬
- **공고 수집**: `fetch_all()` → `deduplicate_by_link` → `insert_job` 반복
- **샘플 데이터 로드**: `insert_sample_jobs()` 6건 (소스별)
- 메인: `get_jobs(filters)` → st.dataframe (title, source, deadline, keywords_matched, link)

---

## 데이터 흐름

```
7개 소스 (swuniv, codeit, likelion, modulabs, fastcampus, elice, careerly)
  → registry.fetch_all() → deduplicate_by_link → insert_job → get_jobs → st.dataframe
```

**job dict 스키마:** `{title, link, source, deadline, posted_at, description, keywords_matched}`

**샘플 job (insert_sample_jobs):**
```python
{"title": "[강사] 파이썬 데이터 분석", "link": "https://example.com/sample1", "source": "swuniv",
 "deadline": "2025-04-15", "posted_at": "2025-03-01", "description": "", "keywords_matched": "파이썬, 데이터 분석"}
{"title": "[강사] AI 에이전트 교육", "link": "https://example.com/sample2", "source": "swuniv",
 "deadline": "2025-04-30", "posted_at": "2025-03-02", "description": "", "keywords_matched": "AI 에이전트"}
```

---

## 검증 명령
- 1: `python -c "from config import KEYWORDS; assert len(KEYWORDS) >= 6"`
- 2: `python -c "from database.db_handler import init_db, insert_job, get_jobs; init_db(); insert_job({'title':'t','link':'https://x.com/1','source':'swuniv','deadline':'2025-04-01','posted_at':'','description':'','keywords_matched':''}); print(len(get_jobs()))"`
- 3: `python -c "from utils.date_parser import parse_deadline; from utils.deduplicator import deduplicate_by_link; assert parse_deadline('2025-03-31'); assert len(deduplicate_by_link([{'link':'a'},{'link':'a'}]))==1"`
- 4: `python -c "from scrapers.registry import fetch_all; j=fetch_all(); print('OK:', len(j), 'sources:', set(x['source'] for x in j))"`
- 5: `streamlit run app.py` → 수집 → 목록 표시

**Phase 2:** API 키 승인 시 saramin_scrp 등 추가. 환경변수: SARAMIN_ACCESS_KEY, WANTED_CLIENT_ID/SECRET, WORKNET_API_KEY, DATA_GO_KR_SERVICE_KEY. 로컬: `copy .streamlit\secrets.toml.example .streamlit\secrets.toml` 후 입력. Streamlit Cloud: 앱 설정 → Secrets 탭.

---

## 주요 기능 (구현됨)

1. **1차 수집 범위 스크래핑**: SW중심대학, 코드잇, 멋사, 모두의연구소, 패스트캠퍼스, 엘리스, 커리어리 (BeautifulSoup + requests)
2. **키워드 필터링**: 8개 키워드, title/keywords_matched OR 검색
3. **마감일 파싱**: YYYY-MM-DD, MM/DD, D일 남음 등 → 표준 형식
4. **중복 제거**: link 기준, URL 정규화(utm_ 등 제거), DB ON CONFLICT 갱신

---

## 기술 스택

Python 3.10+, Streamlit, BeautifulSoup4, requests, SQLite, Pandas

**requirements.txt:** streamlit, pandas, requests, beautifulsoup4, lxml (swuniv는 html.parser 사용)

---

## 프로젝트 구조

```text
.
├── app.py              # Streamlit 진입점
├── config.py           # KEYWORDS, DB_PATH, SWUNIV_URL, get_api_key
├── requirements.txt
├── scrapers/
│   ├── _base.py        # 공통 fetch_html, parse_html, sleep
│   ├── registry.py    # fetch_all() 통합 수집
│   ├── swuniv_scrp.py # SW중심대학
│   ├── codeit_scrp.py # 코드잇
│   ├── likelion_scrp.py # 멋쟁이사자처럼
│   ├── modulabs_scrp.py # 모두의연구소
│   ├── fastcampus_scrp.py # 패스트캠퍼스
│   ├── elice_scrp.py  # 엘리스
│   └── careerly_scrp.py # 커리어리
├── database/
│   ├── db_handler.py   # init_db, insert_job, get_jobs, insert_sample_jobs
│   └── schema.sql
└── utils/
    ├── date_parser.py  # parse_deadline
    ├── deduplicator.py # deduplicate_by_link
    └── text_cleaner.py # clean_html, match_keywords
```

---

## 데이터베이스

**jobs:** id, title, link(UNIQUE), source, deadline, posted_at, description, keywords_matched, created_at

**scrape_logs:** Phase 2+용 (id, source, status, message, created_at)

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
