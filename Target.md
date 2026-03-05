# Scraping Targets & Data Sources

강사 채용 공고 수집 앱의 데이터 소스 및 수집 방법을 정의합니다.

---

## 공통 검색 키워드

| 키워드 | 용도 |
|--------|------|
| 바이브코딩 | 대학/교육기관 강의 도구 |
| 파이썬 데이터 분석 | 데이터 분석 강사 |
| AI 에이전트 | AI/ML 강사 |
| 데이터 분석 강사 | 직무 검색 |
| AI 교육 | 교육 분야 |
| 파이썬 코딩 | 프로그래밍 강사 |
| 머신러닝 강사 | ML 분야 |
| 딥러닝 강사 | DL 분야 |

---

## 1. 채용 플랫폼 (General)

### 1.1 사람인 (Saramin)

| 항목 | 내용 |
|------|------|
| URL | https://www.saramin.co.kr |
| API | **O** `https://oapi.saramin.co.kr/job-search` |
| 수집 방법 | **API 우선** (스크래핑 불필요) |
| API 키 | [사람인 개발자센터](https://oapi.saramin.co.kr)에서 발급 |
| 검색 파라미터 | `keywords` (데이터 분석 강사, AI 교육, 파이썬 코딩 등) |
| 비고 | 공식 API로 안정적. robots.txt 이슈 없음. |
| 응답→jobs 매핑 | `jobs.job[]` → title, url, deadline, expiration-date 등 → DB 스키마 변환 |

### 1.2 잡코리아 (Jobkorea)

| 항목 | 내용 |
|------|------|
| URL | https://www.jobkorea.co.kr |
| API | **O** [잡코리아 API](https://www.jobkorea.co.kr/service/api) |
| 수집 방법 | API 신청 가능 시 API, 불가 시 **검색 URL 스크래핑** |
| API 제한 | 공공기관/학교 우선, 기업/개인은 내부검토 |
| 검색 URL | `https://www.jobkorea.co.kr/Search?stext={키워드}` |
| 필터 | 교육/강사 카테고리 활용 |
| 비고 | API 미승인 시 BeautifulSoup으로 검색 결과 페이지 수집. |

### 1.3 원티드 (Wanted)

| 항목 | 내용 |
|------|------|
| URL | https://www.wanted.co.kr |
| API | **O** [원티드 OpenAPI](https://openapi.wanted.jobs) |
| 수집 방법 | **API 우선** |
| API 신청 | [openapi.wanted.jobs/apply](https://openapi.wanted.jobs/apply/) |
| 비고 | 실무형 멘토, 프로젝트 기반 강사 위주. 인증키(client-ID, client-secret) 필요. |

---

## 2. 공공 및 교육기관 (Public & Academic)

### 2.1 워크넷 (Worknet)

| 항목 | 내용 |
|------|------|
| URL | https://www.worknet.go.kr |
| API | **O** 고용24 OPEN-API (통합) |
| 수집 방법 | **API 우선** |
| API 신청 | [고용24 OPEN-API](https://www.work24.go.kr) 회원가입 후 인증키 신청 |
| 비고 | 고용노동부 공식. 채용정보 API 제공. |

### 2.2 나라장터 (G2B)

| 항목 | 내용 |
|------|------|
| URL | https://www.g2b.go.kr |
| API | **O** 공공데이터포털 |
| 수집 방법 | **API 우선** |
| API 신청 | [공공데이터포털](https://www.data.go.kr) → "조달청 입찰공고" 검색 → 활용신청 |
| 비고 | 교육 용역 입찰 공고. 키워드로 "교육", "강사", "SW" 등 필터링. |

### 2.3 SW중심대학 사업단 협의회

| 항목 | 내용 |
|------|------|
| URL | http://www.swuniv.kr |
| API | **X** |
| 수집 방법 | **HTML 스크래핑** |
| 채용 페이지 | `http://www.swuniv.kr/59/` (소식 > 채용·입찰) |
| 비고 | 각 선정대학 SW중심대학사업단 직원/강사 채용 공고. |

### 2.4 개별 대학 CTL/산학협력단

| 항목 | 내용 |
|------|------|
| 대상 | 삼육대, 건국대, 성균관대 등 (바이브코딩 도입·활용 대학) |
| API | **X** |
| 수집 방법 | **HTML 스크래핑** (대학별 채용/산학협력단 페이지) |
| 비고 | 대학마다 URL·구조 상이. 사이트별 스크래퍼 필요. |

---

## 3. 민간 IT 아카데미 (Private)

| 사이트 | URL | API | 수집 방법 | 비고 |
|--------|-----|-----|-----------|------|
| 패스트캠퍼스 | https://fastcampus.co.kr | X | HTML 스크래핑 | 채용/강사 페이지 탐색 |
| 엘리스 (Elice) | https://elice.io | X | HTML 스크래핑 | 채용 섹션 |
| 멋쟁이사자처럼 | https://likelion.net | X | HTML 스크래핑 | 채용/운영진 페이지 |
| 코드잇 (Codeit) | https://www.codeit.kr | X | HTML 스크래핑 | 채용 페이지 |

- 공통: 채용 공고가 메인 페이지가 아닌 별도 섹션에 있을 수 있음. 사이트마다 구조 확인 필요.
- JS 렌더링 사용 시 Selenium/Playwright 고려.

---

## 4. 커뮤니티 (Community)

| 사이트 | URL | API | 수집 방법 | 비고 |
|--------|-----|-----|-----------|------|
| 커리어리 (Careerly) | https://careerly.co.kr | X | HTML 스크래핑 | 개발자 커뮤니티, 채용 섹션 확인 |
| 모두의연구소 | https://modulabs.co.kr | X | HTML 스크래핑 | AI/로봇 교육, 채용/멘토 페이지 |
| 링크드인 (LinkedIn) | https://www.linkedin.com | O | API (Phase 3) | 인증 복잡. 우선순위 낮음. |

---

## 수집 방법 요약

| 수집 방법 | 적용 대상 | 비고 |
|-----------|-----------|------|
| **API** | 사람인, 원티드, 워크넷, 나라장터 | 인증키/API 키 필요. 최우선 사용. |
| **API (신청 제한)** | 잡코리아 | 공공기관 우선. 미승인 시 스크래핑. |
| **HTML 스크래핑** | SW중심대학, 개별 대학, 패스트캠퍼스, 엘리스, 멋사, 코드잇, 커리어리, 모두의연구소 | BeautifulSoup. JS 필요 시 Selenium/Playwright. |

---

## 준수 사항

- 각 사이트 `robots.txt` 확인 후 크롤링 규칙 준수
- API 제공 시 **API 우선** 활용
- 스크래핑 시: 요청 간격 2초 이상, User-Agent 설정, 순차 실행
- API 키·인증키는 환경변수로 관리, 코드에 하드코딩 금지
