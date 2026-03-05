"""1차 수집 범위 스크래퍼 등록 및 통합 수집."""

from scrapers.swuniv_scrp import fetch as fetch_swuniv
from scrapers.codeit_scrp import fetch as fetch_codeit
from scrapers.likelion_scrp import fetch as fetch_likelion
from scrapers.modulabs_scrp import fetch as fetch_modulabs
from scrapers.fastcampus_scrp import fetch as fetch_fastcampus
from scrapers.elice_scrp import fetch as fetch_elice
from scrapers.careerly_scrp import fetch as fetch_careerly

# 1차 수집 범위: Target.md MVP HTML 스크래핑 대상
SCRAPERS = [
    ("swuniv", fetch_swuniv),
    ("codeit", fetch_codeit),
    ("likelion", fetch_likelion),
    ("modulabs", fetch_modulabs),
    ("fastcampus", fetch_fastcampus),
    ("elice", fetch_elice),
    ("careerly", fetch_careerly),
]


def fetch_all() -> list[dict]:
    """모든 1차 수집 대상에서 공고 수집. (source, jobs) 튜플 리스트 반환."""
    all_jobs = []
    for source_name, fetch_fn in SCRAPERS:
        try:
            jobs = fetch_fn()
            for j in jobs:
                j["source"] = source_name
                all_jobs.append(j)
        except Exception:
            pass
    return all_jobs
