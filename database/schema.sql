-- jobs: 공고 메타데이터
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    deadline TEXT,
    posted_at TEXT,
    description TEXT,
    keywords_matched TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_deadline ON jobs(deadline);

-- scrape_logs: 수집 이력 (Phase 2+)
CREATE TABLE IF NOT EXISTS scrape_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);
