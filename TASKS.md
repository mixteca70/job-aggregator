# 작업자 필수 작업 목록

API 키 수령 후 및 단계별 개발 시 수행할 작업을 순서대로 정리합니다.

---

## API 키 수령 후 필수 작업

### 1. API 키 저장 (로컬 개발)

| 순서 | 작업 | 방법 |
|------|------|------|
| 1 | `.streamlit/secrets.toml.example` 복사 | `copy .streamlit\secrets.toml.example .streamlit\secrets.toml` (Windows) |
| 2 | `secrets.toml` 열기 | 텍스트 에디터로 열기 |
| 3 | API 키 입력 | `SARAMIN_ACCESS_KEY = "발급받은-키-붙여넣기"` |
| 4 | 저장 | `secrets.toml` 저장 (이 파일은 .gitignore에 포함되어 커밋되지 않음) |

**또는 환경변수 사용 (PowerShell):**
```powershell
$env:SARAMIN_ACCESS_KEY = "발급받은-키"
```

### 2. API 키 저장 (Streamlit Cloud 배포)

| 순서 | 작업 | 방법 |
|------|------|------|
| 1 | share.streamlit.io 접속 | 앱 설정 → Secrets 탭 |
| 2 | Secrets 편집 | 아래 형식 입력 |
| 3 | 저장 | 자동 적용 |

```toml
SARAMIN_ACCESS_KEY = "발급받은-키"
```

---

## 단계별 개발 작업 순서

| 단계 | 작업 | 완료 | 비고 |
|------|------|------|------|
| 0 | 프로젝트 초기화 | O | 완료 |
| 1 | config.py 작성 | O | KEYWORDS, SARAMIN_API_URL, DB_PATH, get_api_key |
| 2 | db_handler.py 작성 | | init_db, insert_job, get_jobs |
| 3 | utils 모듈 작성 | | date_parser, deduplicator, text_cleaner |
| 4 | saramin_scrp.py 작성 | | fetch() |
| 5 | app.py 완성 | | 수집, 목록, 필터, 정렬 |

---

## 각 단계 완료 후 검증

| 단계 | 검증 명령 |
|------|-----------|
| 1 | `python -c "from config import KEYWORDS; assert len(KEYWORDS) >= 6"` |
| 2 | `python -c "from database.db_handler import init_db, insert_job, get_jobs; init_db(); insert_job({'title':'t','link':'https://x.com/1','source':'saramin','deadline':'2025-04-01','posted_at':'','description':'','keywords_matched':''}); print(len(get_jobs()))"` |
| 3 | `python -c "from utils.date_parser import parse_deadline; from utils.deduplicator import deduplicate_by_link; assert parse_deadline('2025-03-31'); assert len(deduplicate_by_link([{'link':'a'},{'link':'a'}]))==1"` |
| 4 | `python -c "from scrapers.saramin_scrp import fetch; r=fetch(['데이터'], None); print('OK' if r==[] else len(r))"` |
| 5 | `streamlit run app.py` → 수집 또는 샘플 로드 → 목록 표시 확인 |
