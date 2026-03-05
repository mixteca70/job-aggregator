# 반복 오류 및 해결 (Troubleshooting)

개발 중 자주 발생하는 오류와 해결 방법을 기록합니다. 동일 실수를 반복하지 않도록 참조하세요.

---

## API 키 관련

| 오류/증상 | 원인 | 해결 |
|-----------|------|------|
| API 401 Unauthorized | API 키 미설정 또는 잘못된 키 | `SARAMIN_ACCESS_KEY` 환경변수 또는 `.streamlit/secrets.toml` 확인 |
| fetch() 빈 리스트만 반환 | API 키가 None/빈 문자열 | TASKS.md "API 키 저장" 절차 수행 |
| secrets.toml 인식 안 됨 | 파일 위치 오류 | `.streamlit/secrets.toml` (프로젝트 루트 하위)에 위치 확인 |
| API 키가 Git에 커밋됨 | secrets.toml이 .gitignore 제외 | `.gitignore`에 `secrets.toml` 포함 확인, 이미 커밋 시 `git rm --cached` 후 재커밋 |

---

## Python / Import 관련

| 오류/증상 | 원인 | 해결 |
|-----------|------|------|
| ModuleNotFoundError: No module named 'config' | 프로젝트 루트에서 실행 안 함 | `cd d:\job` 후 실행 |
| ModuleNotFoundError: No module named 'scrapers' | __init__.py 없음 | scrapers/, database/, utils/ 각각 __init__.py 존재 확인 |
| ImportError (순환 참조) | config에서 streamlit import | get_api_key()에서 st.secrets 사용 시 streamlit import는 함수 내부에서만 |

---

## 데이터베이스 관련

| 오류/증상 | 원인 | 해결 |
|-----------|------|------|
| sqlite3.OperationalError: database is locked | 다른 프로세스가 DB 사용 중 | Streamlit 앱 종료 후 재시도, 또는 DB 연결 close 확인 |
| no such table: jobs | init_db() 미실행 | `init_db()` 먼저 호출 |
| UNIQUE constraint failed: jobs.link | 동일 link 중복 insert | INSERT OR REPLACE 또는 ON CONFLICT 사용 |

---

## Streamlit 관련

| 오류/증상 | 원인 | 해결 |
|-----------|------|------|
| st.secrets 오류 (로컬) | secrets.toml 없음 | secrets.toml.example 복사 후 secrets.toml 생성 |
| 앱이 갱신되지 않음 | 캐시 | 브라우저 새로고침, 또는 streamlit run 재시작 |
| 포트 8501 이미 사용 | 이전 프로세스 대기 중 | `Ctrl+C`로 종료 후 재실행 |

---

## 추가 오류 기록

(새 오류 발생 시 위 표에 항목 추가)
