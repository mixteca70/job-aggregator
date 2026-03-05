# AI/Data Instructor Job Aggregator & Scheduler

웹에서 데이터 분석, 머신러닝, 딥러닝 강사 및 교육 공고를 수집하고 지원 일정을 관리하는 Streamlit 기반 웹앱입니다.

---

## 빠른 시작

```bash
git clone https://github.com/YOUR_USERNAME/job-aggregator.git
cd job-aggregator
pip install -r requirements.txt
# API 키 설정: $env:SARAMIN_ACCESS_KEY="your-key" (Windows)
streamlit run app.py
```

- **개발 가이드**: [GUIDE.md](GUIDE.md) (협업, 배포, 단계별 구현·테스트)
- **작업 목록**: [TASKS.md](TASKS.md) (API 키 저장, 단계별 필수 작업)
- **오류 해결**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) (반복 오류 기록)
- **구현 전**: GUIDE.md 단계 0~5 순서대로 진행
- **API 키 발급 지연 시**: 단계 1~3 → 4(구조) → 5(샘플 데이터로 UI 검증) 순으로 진행 가능

---

## 주요 기능

1. **Multi-Source Scraping**: `Target.md`에 정의된 사이트에서 최신 공고 자동 수집
2. **Keyword Filtering**: '바이브코딩', '파이썬 데이터 분석', 'AI 에이전트' 등 핵심 키워드 매칭
3. **Smart Scheduling**: 수집된 마감일을 추출하여 캘린더 뷰에 자동 표시
4. **Duplicate Handling**: 중복 공고 자동 필터링 (Link 기준)

---

## 기술 스택

| 구분 | 기술 | 비고 |
|------|------|------|
| Language | Python 3.10+ | |
| Frontend | Streamlit | |
| API/HTTP | requests | Phase 1 (사람인 API) |
| Scraping | BeautifulSoup4 | Phase 2+ 스크래핑 시 |
| Scraping (선택) | Selenium, Playwright | JS 렌더링, Phase 2+ |
| Database | SQLite | 파일 기반, 마이그레이션 불필요 |
| Analysis | Pandas | |

---

## 프로젝트 구조

```text
.
├── app.py                    # Streamlit 메인 진입점
├── config.py                 # 키워드, URL, 설정 상수
├── requirements.txt          # 의존성 목록
├── README.md                 # 프로젝트 문서 (본 문서)
├── Target.md                 # 수집 대상 및 수집 방법
├── GUIDE.md                  # 협업, 배포, 구현·테스트 가이드
├── TASKS.md                  # 작업자 필수 작업 (API 키 저장, 단계별)
├── TROUBLESHOOTING.md        # 반복 오류 및 해결
├── .gitignore
├── .streamlit/
│   ├── config.toml           # Streamlit 설정
│   └── secrets.toml.example  # API 키 예시 (복사 후 사용)
├── .github/
│   ├── ISSUE_TEMPLATE/       # 이슈 템플릿
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/test.yml    # pytest (tests/ 존재 시)
│
├── scrapers/
│   ├── __init__.py
│   ├── base.py               # 공통 BaseScraper 인터페이스
│   ├── saramin_scrp.py       # 사람인 (API)
│   ├── jobkorea_scrp.py      # 잡코리아 (API 또는 스크래핑)
│   ├── wanted_scrp.py        # 원티드 (API)
│   ├── worknet_scrp.py       # 워크넷 (API)
│   ├── g2b_scrp.py           # 나라장터 (API)
│   ├── swuniv_scrp.py        # SW중심대학 (스크래핑)
│   ├── univ_scrp.py          # 개별 대학 CTL/산학협력단 (스크래핑)
│   ├── academy_scrp.py       # 패스트캠퍼스, 엘리스, 멋사, 코드잇 (스크래핑)
│   └── community_scrp.py     # 커리어리, 모두의연구소, 링크드인 (스크래핑/API)
│
├── database/
│   ├── __init__.py
│   ├── db_handler.py         # CRUD, 연결 관리
│   └── schema.sql            # 테이블 스키마
│
└── utils/
    ├── __init__.py
    ├── date_parser.py        # 마감일 추출/정규화
    ├── deduplicator.py       # Link 기준 중복 제거
    └── text_cleaner.py       # HTML 제거, 키워드 매칭용 정규화
```

---

## 데이터 소스 (Target.md 기반)

| 카테고리 | 사이트 | 수집 방법 | API/키 | 우선순위 |
|----------|--------|-----------|--------|----------|
| 채용 플랫폼 | 사람인 | API | oapi.saramin.co.kr | P0 |
| 채용 플랫폼 | 잡코리아 | API 또는 스크래핑 | API 공공기관 우선 | P0 |
| 채용 플랫폼 | 원티드 | API | openapi.wanted.jobs | P1 |
| 공공/교육 | 워크넷 | API | 고용24 OPEN-API | P1 |
| 공공/교육 | 나라장터 | API | 공공데이터포털 | P1 |
| 공공/교육 | SW중심대학 | 스크래핑 | - | P2 |
| 공공/교육 | 개별 대학 | 스크래핑 | - | P2 |
| 민간 아카데미 | 패스트캠퍼스, 엘리스, 멋사, 코드잇 | 스크래핑 | - | P2 |
| 커뮤니티 | 커리어리, 모두의연구소 | 스크래핑 | - | P3 |
| 커뮤니티 | 링크드인 | API (Phase 3) | 인증 복잡 | P3 |

상세 URL, 검색 키워드, API 신청 절차는 [Target.md](Target.md) 참조.

---

## 데이터베이스 스키마

### jobs 테이블

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | 자동 증가 |
| title | TEXT | 공고 제목 |
| link | TEXT UNIQUE | 공고 URL (중복 판별 기준) |
| source | TEXT | 수집 소스명 (saramin, jobkorea 등) |
| deadline | TEXT | 마감일 (ISO 8601: YYYY-MM-DD) |
| posted_at | TEXT | 게시일 |
| description | TEXT | 본문 요약 (선택) |
| keywords_matched | TEXT | 매칭된 키워드 (쉼표 구분) |
| created_at | TEXT | DB 저장 시각 |

### scrape_logs 테이블 (선택)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | |
| source | TEXT | |
| status | TEXT | success / partial / failed |
| message | TEXT | 에러 메시지 |
| created_at | TEXT | |

---

## 프로토타입 구현 단계 (Phase 구분)

### Phase 1 - MVP (최소 기능 제품)

- **목표**: 1개 소스에서 공고 수집 → DB 저장 → 목록 표시
- **스크래퍼**: 사람인 1개만 (API 사용, 스크래핑 불필요)
- **UI**: 공고 목록, 키워드 필터, 마감일 정렬
- **캘린더**: Phase 2로 연기 (단순 테이블로 대체)
- **의존성**: streamlit, pandas, requests (API만 사용 시 BeautifulSoup 불필요)

### Phase 2 - 확장

- 원티드, 워크넷, 나라장터 API 연동
- 잡코리아 (API 또는 스크래핑)
- `streamlit-calendar` 패키지로 캘린더 뷰
- Selenium/Playwright (JS 렌더링 필요 시)

### Phase 3 - 고도화

- SW중심대학, 개별 대학, 민간 아카데미, 커뮤니티 스크래퍼
- 설정 페이지, 스케줄러 연동

---

## API 연동 환경변수

| 소스 | 환경변수 | 비고 |
|------|----------|------|
| 사람인 | `SARAMIN_ACCESS_KEY` | [사람인 개발자센터](https://oapi.saramin.co.kr) |
| 원티드 | `WANTED_CLIENT_ID`, `WANTED_CLIENT_SECRET` | [원티드 OpenAPI](https://openapi.wanted.jobs/apply) |
| 워크넷 | `WORKNET_API_KEY` | [고용24 OPEN-API](https://www.work24.go.kr) |
| 나라장터 | `DATA_GO_KR_SERVICE_KEY` | [공공데이터포털](https://www.data.go.kr) |

---

## 스크래퍼 구현 시 주의사항

### 1. API 우선 사용

- 사람인, 원티드, 워크넷, 나라장터는 API 제공. **API 우선** 사용.
- 잡코리아 API는 공공기관/학교 우선. 미승인 시 검색 URL 스크래핑.

### 2. 스크래핑 시 필수

- **요청 간격**: 소스당 최소 2초 이상
- **순차 실행**: 여러 스크래퍼 동시 실행 금지
- **User-Agent**: `Mozilla/5.0 ...` 형태로 설정
- **robots.txt**: 각 도메인 확인 후 준수

### 3. 에러 처리

- 개별 스크래퍼 실패 시 해당 소스만 스킵
- `scrape_logs`에 실패 이력 기록
- 재시도: 최대 2회, 지수 백오프 (1초 → 2초)

### 4. HTML 구조 변경 대비

- CSS 선택자는 `config.py` 또는 스크래퍼 상단에 상수로 분리

---

## 설치 및 실행

### 1. 가상환경 생성 (권장)

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 (API 사용 시)

```powershell
# Windows - 사람인 예시
$env:SARAMIN_ACCESS_KEY = "your-api-key"
```

```bash
# Linux / macOS
export SARAMIN_ACCESS_KEY="your-api-key"
```

### 4. 실행

```bash
streamlit run app.py
```

---

## requirements.txt (권장 구성)

```text
# 필수 (Phase 1 - API만 사용 시)
streamlit>=1.28.0
pandas>=2.0.0
requests>=2.31.0

# 스크래핑 시 추가
# beautifulsoup4>=4.12.0
# lxml>=4.9.0

# 선택 (Phase 2+, JS 렌더링 필요 시)
# selenium>=4.15.0
# playwright>=1.40.0
```

---

## 캘린더 뷰 구현 가이드

- **Phase 1**: `st.dataframe` + `st.selectbox`(월 선택) + 마감일 정렬 목록
- **Phase 2**: `streamlit-calendar` 패키지 (`pip install streamlit-calendar`)
- **대안**: `st.date_input`으로 날짜 범위 필터 후 테이블 표시

---

## 중복 제거 규칙

- **기준**: `link` 필드
- **정규화**: URL 쿼리 파라미터 중 `utm_*`, `ref` 등 제거 후 비교
- **저장 시**: `INSERT OR REPLACE` 또는 `ON CONFLICT(link) DO UPDATE` 활용

---

## GitHub 및 배포

- **저장소**: GitHub push → [Streamlit Community Cloud](https://share.streamlit.io) 무료 배포
- **협업·배포·테스트**: [GUIDE.md](GUIDE.md) 참조

---

## 참고 문서

- [Target.md](Target.md): 수집 대상 사이트, 검색 키워드, 수집 방법 상세
- [사람인 API 가이드](https://oapi.saramin.co.kr/guide/job-search)
- [원티드 OpenAPI](https://openapi.wanted.jobs)
- [고용24 OPEN-API](https://www.work24.go.kr)
- [공공데이터포털](https://www.data.go.kr)
