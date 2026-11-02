import sqlite3
import os
import json
from typing import List, Optional, Dict
from domain.entities.content_item import ContentItem, LaunchStrategy, AvailabilityStatus
from domain.entities.viewing_history import ViewingHistoryRecord, EventSource, CompletionStatus
from domain.entities.user_profile import UserProfile, InteractionPreferences
from application.ports.repository_ports import (
    ContentRepositoryPort,
    HistoryRepositoryPort,
    PreferenceRepositoryPort
)


class SqliteRepositoryAdapter(
    ContentRepositoryPort,
    HistoryRepositoryPort,
    PreferenceRepositoryPort
):
    """
    SQLite Persistence Adapter:
    Lưu trữ toàn bộ dữ liệu Content Catalog, Viewing History và User Preferences
    trong 1 file sqlite cục bộ (data/context_db.sqlite).
    """

    def __init__(self, db_path: str = "data/context_db.sqlite"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 1. Bảng danh mục nội dung
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_catalog (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                provider TEXT NOT NULL,
                launch_strategy TEXT NOT NULL,
                deep_link TEXT,
                workflow_steps TEXT,
                speaker_or_artist TEXT,
                tags TEXT,
                availability TEXT DEFAULT 'AVAILABLE',
                default_priority INTEGER DEFAULT 50,
                last_verified TIMESTAMP
            );
            """)

            # 2. Bảng lịch sử xem
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS viewing_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT DEFAULT 'grandmother',
                content_id TEXT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                event_type TEXT DEFAULT 'PLAYED',
                source TEXT NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                duration_seconds INTEGER DEFAULT 0,
                completion_status TEXT DEFAULT 'UNKNOWN',
                was_skipped_immediately BOOLEAN DEFAULT 0,
                raw_utterance TEXT,
                FOREIGN KEY(content_id) REFERENCES content_catalog(id)
            );
            """)

            # 3. Bảng điểm sở thích
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT NOT NULL,
                item_key TEXT NOT NULL,
                item_type TEXT NOT NULL,
                score REAL DEFAULT 50.0,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, item_key)
            );
            """)
            conn.commit()

    # -------------------------------------------------------------
    # ContentRepositoryPort Implementation
    # -------------------------------------------------------------
    def get_by_id(self, content_id: str) -> Optional[ContentItem]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM content_catalog WHERE id = ?", (content_id,)).fetchone()
            if row:
                return self._row_to_content_item(row)
        return None

    def search_by_category(self, category: str, limit: int = 5) -> List[ContentItem]:
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM content_catalog WHERE category = ? ORDER BY default_priority DESC LIMIT ?",
                (category.upper(), limit)
            ).fetchall()
            return [self._row_to_content_item(r) for r in rows]

    def search_by_keyword(self, keyword: str, limit: int = 5) -> List[ContentItem]:
        kw = f"%{keyword.lower().strip()}%"
        with self._get_connection() as conn:
            rows = conn.execute(
                """SELECT * FROM content_catalog 
                   WHERE LOWER(name) LIKE ? OR LOWER(speaker_or_artist) LIKE ? OR LOWER(tags) LIKE ?
                   ORDER BY default_priority DESC LIMIT ?""",
                (kw, kw, kw, limit)
            ).fetchall()
            return [self._row_to_content_item(r) for r in rows]

    def list_all(self) -> List[ContentItem]:
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM content_catalog ORDER BY default_priority DESC").fetchall()
            return [self._row_to_content_item(r) for r in rows]

    def save(self, item: ContentItem) -> bool:
        with self._get_connection() as conn:
            conn.execute("""
            INSERT INTO content_catalog (
                id, name, category, provider, launch_strategy, deep_link,
                workflow_steps, speaker_or_artist, tags, availability, default_priority, last_verified
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                category=excluded.category,
                deep_link=excluded.deep_link,
                speaker_or_artist=excluded.speaker_or_artist,
                tags=excluded.tags,
                default_priority=excluded.default_priority
            """, (
                item.id,
                item.name,
                item.category,
                item.provider,
                item.launch_strategy.value,
                item.deep_link,
                json.dumps(item.workflow_steps, ensure_ascii=False),
                item.speaker_or_artist,
                ",".join(item.tags),
                item.availability.value,
                item.default_priority,
                item.last_verified
            ))
            conn.commit()
            return True

    def _row_to_content_item(self, row: sqlite3.Row) -> ContentItem:
        tags_raw = row["tags"] or ""
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        steps_raw = row["workflow_steps"] or "[]"
        try:
            steps = json.loads(steps_raw)
        except Exception:
            steps = []

        return ContentItem(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            provider=row["provider"],
            launch_strategy=LaunchStrategy(row["launch_strategy"]),
            deep_link=row["deep_link"],
            workflow_steps=steps,
            speaker_or_artist=row["speaker_or_artist"],
            tags=tags,
            availability=AvailabilityStatus(row["availability"]),
            default_priority=row["default_priority"],
            last_verified=row["last_verified"]
        )

    # -------------------------------------------------------------
    # HistoryRepositoryPort Implementation
    # -------------------------------------------------------------
    def record_event(self, record: ViewingHistoryRecord) -> int:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO viewing_history (
                user_id, content_id, title, category, event_type, source,
                duration_seconds, completion_status, was_skipped_immediately, raw_utterance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.user_id,
                record.content_id,
                record.title,
                record.category,
                record.event_type,
                record.source.value,
                record.duration_seconds,
                record.completion_status.value,
                1 if record.was_skipped_immediately else 0,
                record.raw_utterance
            ))
            conn.commit()
            return cur.lastrowid

    def get_recent_history(self, user_id: str = "grandmother", limit: int = 10) -> List[ViewingHistoryRecord]:
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM viewing_history WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit)
            ).fetchall()
            return [self._row_to_history_record(r) for r in rows]

    def get_history_by_temporal_range(self, start_date_str: str, end_date_str: str) -> List[ViewingHistoryRecord]:
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM viewing_history WHERE started_at BETWEEN ? AND ? ORDER BY id DESC",
                (start_date_str, end_date_str)
            ).fetchall()
            return [self._row_to_history_record(r) for r in rows]

    def get_last_played(self, user_id: str = "grandmother") -> Optional[ViewingHistoryRecord]:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM viewing_history WHERE user_id = ? ORDER BY id DESC LIMIT 1",
                (user_id,)
            ).fetchone()
            if row:
                return self._row_to_history_record(row)
        return None

    def _row_to_history_record(self, row: sqlite3.Row) -> ViewingHistoryRecord:
        return ViewingHistoryRecord(
            id=row["id"],
            user_id=row["user_id"],
            content_id=row["content_id"],
            title=row["title"],
            category=row["category"],
            event_type=row["event_type"],
            source=EventSource(row["source"]),
            started_at=str(row["started_at"]),
            ended_at=str(row["ended_at"]) if row["ended_at"] else None,
            duration_seconds=row["duration_seconds"] or 0,
            completion_status=CompletionStatus(row["completion_status"]),
            was_skipped_immediately=bool(row["was_skipped_immediately"]),
            raw_utterance=row["raw_utterance"] or ""
        )

    # -------------------------------------------------------------
    # PreferenceRepositoryPort Implementation
    # -------------------------------------------------------------
    def get_user_profile(self, user_id: str = "grandmother") -> UserProfile:
        scores = self.get_preference_scores(user_id)
        return UserProfile(
            user_id=user_id,
            category_scores=scores
        )

    def update_preference_score(self, user_id: str, item_key: str, item_type: str, delta: float) -> float:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT score FROM user_preferences WHERE user_id = ? AND item_key = ?",
                (user_id, item_key)
            ).fetchone()
            current_score = row["score"] if row else 50.0
            new_score = max(0.0, min(100.0, current_score + delta))

            conn.execute("""
            INSERT INTO user_preferences (user_id, item_key, item_type, score, last_interaction)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, item_key) DO UPDATE SET
                score=excluded.score,
                last_interaction=CURRENT_TIMESTAMP
            """, (user_id, item_key, item_type, new_score))
            conn.commit()
            return new_score

    def get_preference_scores(self, user_id: str = "grandmother") -> Dict[str, float]:
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT item_key, score FROM user_preferences WHERE user_id = ?",
                (user_id,)
            ).fetchall()
            return {r["item_key"]: float(r["score"]) for r in rows}

