# 개발 가이드 (Development Guide)

협업, 배포, 단계별 구현 및 테스트를 통합한 가이드입니다.

---

## 1. 협업 (Contributing)

### 브랜치 전략

| 브랜치 | 용도 |
|--------|------|
| `main` | 배포용 |
| `develop` | 개발 통합 |
| `feature/xxx`, `fix/xxx` | 기능/수정 |

### 기여 절차

```bash
git clone https://github.com/mixteca70/job-aggregator.git
git checkout -b feature/add-scraper
# 작업 후
git add . && git commit -m "feat: 스크래퍼 추가"
git push origin feature/add-scraper
# PR 생성
```

- 커밋: `feat`, `fix`, `docs`, `refactor`, `test` 타입 사용
- PR 전: 아래 단계별 테스트 통과 확인

---

## 2. API 키 저장 (키 수령 후 필수)

| 환경 | 저장 위치 | 방법 |
|------|------------|------|
| 로컬 | `.streamlit/secrets.toml` | `secrets.toml.example` 복사 → `SARAMIN_ACCESS_KEY = "발급키"` 입력 |
| 로컬 (대안) | 환경변수 | `$env:SARAMIN_ACCESS_KEY = "발급키"` (PowerShell) |
| Streamlit Cloud | 앱 Secrets | share.streamlit.io → 앱 설정 → Secrets 탭에 동일 형식 입력 |

**주의:** `secrets.toml`은 .gitignore에 포함됨. 코드에 API 키 하드코딩 금지. 상세는 [TASKS.md](TASKS.md) 참조.

---

## 3. 배포 (Deployment)

### Streamlit Community Cloud (무료, 권장)

1. [share.streamlit.io](https://share.streamlit.io) → GitHub 로그인
2. New app → Repository, Branch(`main`), Main file(`app.py`) 선택
3. Secrets에 API 키 입력:

```toml
SARAMIN_ACCESS_KEY = "your-api-key"
```

4. 배포 완료. URL: `https://YOUR_APP.streamlit.app`

### 대안

- **Railway**, **Hugging Face Spaces**: `requirements.txt` 기반 배포 가능
- **로컬**: `pip install -r requirements.txt` → `streamlit run app.py`

---

## 4. 단계별 구현 및 테스트

### API 키 없이 진행 가능한 작업

| 단계 | 구현 대상 | API 키 필요 | 비고 |
|------|-----------|-------------|------|
| 0 | 프로젝트 초기화 | X | 완료 |
| 1 | config.py | X | |
| 2 | database | X | |
| 3 | utils | X | |
| 4 | saramin_scrp.py | O (실제 수집 시) | 구조 구현 가능. 키 없으면 fetch() → [] |
| 5 | app.py | O (수집 버튼 시) | UI·필터·정렬은 샘플 데이터로 테스트 가능 |

**권장 순서**: 1 → 2 → 3 → 4(구조) → 5(UI+샘플) → API 키 도착 시 4·5 연동 테스트

### 개요

| 단계 | 구현 대상 | 통과 기준 |
|------|-----------|-----------|
| 0 | 프로젝트 초기화 | scrapers, database, utils import |
| 1 | config.py | KEYWORDS 6개 이상 로드 |
| 2 | database | insert → get, 중복 1건 |
| 3 | utils | parse_deadline, deduplicate, clean_html |
| 4 | saramin_scrp.py | fetch() 1건 이상 (API 키 시) 또는 빈 리스트 반환 (키 없을 때) |
| 5 | app.py | 수집→저장→표시→필터 (API 키 시) 또는 샘플 데이터로 UI 검증 |

### 단계 0: 초기화

- `scrapers/`, `database/`, `utils/` + `__init__.py`, `requirements.txt`
- 테스트: `python -c "import scrapers; import database; import utils"`

### 단계 1: config.py

- `KEYWORDS` (Target.md 8개), `SARAMIN_API_URL`, `DB_PATH`
- API 키 로드: `os.environ.get("SARAMIN_ACCESS_KEY")` 우선, Streamlit 실행 시 `st.secrets.get("SARAMIN_ACCESS_KEY")` fallback
- 테스트: `from config import KEYWORDS; assert len(KEYWORDS) >= 6`

### 단계 2: database

- `schema.sql` (이미 생성됨), `db_handler.py` (init_db, insert_job, get_jobs)
- `get_jobs(filters)` 필터: `keyword`, `source`, `sort` (deadline asc/desc)
- `insert_sample_jobs()` (선택): API 키 없이 UI 테스트용 샘플 2~3건 삽입
- 테스트: `init_db()` → `insert_job({...})` → `get_jobs()` 1건 이상

**샘플 job dict (단일):**
```python
{"title": "테스트", "link": "https://example.com/1", "source": "saramin",
 "deadline": "2025-03-31", "posted_at": "2025-03-01", "description": "",
 "keywords_matched": "데이터 분석 강사"}
```

**샘플 목록 (app.py UI 테스트용, API 키 없을 때):**
```python
[
    {"title": "[강사] 파이썬 데이터 분석", "link": "https://example.com/1", "source": "saramin",
     "deadline": "2025-04-15", "posted_at": "2025-03-01", "description": "", "keywords_matched": "파이썬, 데이터 분석"},
    {"title": "[강사] AI 에이전트 교육", "link": "https://example.com/2", "source": "saramin",
     "deadline": "2025-04-30", "posted_at": "2025-03-02", "description": "", "keywords_matched": "AI 에이전트"},
]
```

### 단계 3: utils

- `date_parser.py`: `parse_deadline(text)` → str|None
- `deduplicator.py`: `deduplicate_by_link(jobs)` → list
- `text_cleaner.py`: `clean_html(text)`, `match_keywords(text, keywords)`
- 테스트: `parse_deadline("2025-03-31")`, `deduplicate_by_link([{link:"a"},{link:"a"}])` → 1건

### 단계 4: scrapers (사람인)

- `saramin_scrp.py`만 구현 (base.py는 Phase 2)
- `fetch(keywords, access_key)` → list[dict], 응답을 jobs 스키마로 변환
- **API 키 없을 때**: `access_key`가 None/빈 문자열이면 `[]` 반환 (에러 없이)
- API: GET, `Accept: application/json`, 파라미터 `keywords`, `access-key`, `count`
- 응답: `jobs.job[]` → 각 항목의 `position`, `url`, `expiration-timestamp` 등 → DB 필드 매핑
- API 키: `os.environ.get("SARAMIN_ACCESS_KEY")` 또는 `st.secrets.get("SARAMIN_ACCESS_KEY")`
- 테스트(키 없음): `fetch(["데이터 분석"], None)` → `[]` 반환
- 테스트(키 있음): `fetch(["데이터 분석"], key)` → 1건 이상

### 단계 5: app.py

- 수집 버튼 → fetch → deduplicate → insert_job → st.dataframe
- 사이드바: 키워드 필터(multiselect), 소스 필터, 마감일 정렬(selectbox)
- **API 키 없을 때**: "샘플 데이터 로드" 버튼으로 테스트용 2~3건 insert → UI·필터·정렬 검증
- 테스트(키 없음): 샘플 로드 → 목록·필터·정렬 동작 확인
- 테스트(키 있음): 수집 버튼 → 실제 공고 표시

### PR 전 체크리스트

- [ ] 단계 0~5 통과
- [ ] API 키 코드에 없음
- [ ] `.gitignore` 대상 미커밋

### 트러블슈팅

자세한 오류·해결은 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 참조.

| 증상 | 확인 |
|------|------|
| API 401 | `SARAMIN_ACCESS_KEY` 환경변수 또는 secrets.toml |
| DB locked | 다른 프로세스 사용 여부 |
| import 에러 | `__init__.py`, PYTHONPATH |

---

## 5. 구현 체크리스트 (Phase 1)

| 단계 | 항목 | 상태 |
|------|------|------|
| 0 | scrapers/, database/, utils/, schema.sql | 완료 |
| 1 | config.py (KEYWORDS, SARAMIN_API_URL, DB_PATH, get_api_key) | 완료 |
| 2 | db_handler.py (init_db, insert_job, get_jobs) | |
| 3 | date_parser, deduplicator, text_cleaner | |
| 4 | saramin_scrp.fetch() | |
| 5 | app.py (수집, 목록, 필터, 정렬) | |

**데이터 흐름:** 사람인 API → fetch → deduplicate → insert_job → get_jobs → st.dataframe

**API 키 발급 지연 시:** 단계 1~3 완료 → 단계 4 fetch()는 키 없으면 [] 반환 → 단계 5에서 샘플 데이터로 UI 검증 → 키 도착 후 수집 기능 테스트
