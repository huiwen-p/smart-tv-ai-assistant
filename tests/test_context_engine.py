import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities.content_item import ContentItem, LaunchStrategy
from domain.entities.viewing_history import ViewingHistoryRecord, EventSource, CompletionStatus
from infrastructure.persistence.sqlite_repository_adapter import SqliteRepositoryAdapter
from application.use_cases.learn_preferences import LearnPreferencesUseCase


class TestContextEngine(unittest.TestCase):
    def setUp(self):
        # Dùng file SQLite tạm thời cho mỗi test case
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite")
        self.temp_db.close()
        self.repo = SqliteRepositoryAdapter(self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            try:
                os.remove(self.temp_db.name)
            except Exception:
                pass

    def test_save_and_retrieve_content(self):
        item = ContentItem(
            id="test_01",
            name="Kinh A Di Đà",
            category="BUDDHIST",
            provider="YOUTUBE",
            launch_strategy=LaunchStrategy.DIRECT_DEEPLINK,
            deep_link="vnd.youtube://mock",
            speaker_or_artist="Thầy Thích Trí Thoát",
            tags=["kinh a di da", "phat phap"],
            default_priority=90
        )
        self.repo.save(item)

        fetched = self.repo.get_by_id("test_01")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Kinh A Di Đà")
        self.assertEqual(fetched.category, "BUDDHIST")
        self.assertEqual(fetched.speaker_or_artist, "Thầy Thích Trí Thoát")

    def test_search_by_category_and_keyword(self):
        item1 = ContentItem(
            id="b1", name="Kinh Dược Sư", category="BUDDHIST", provider="YOUTUBE",
            speaker_or_artist="Thầy Thích Trí Thoát", tags=["cau an"]
        )
        item2 = ContentItem(
            id="n1", name="Thời sự VTV1", category="NEWS", provider="VTVGO",
            speaker_or_artist="VTV", tags=["thoi su"]
        )
        self.repo.save(item1)
        self.repo.save(item2)

        buddhist_list = self.repo.search_by_category("BUDDHIST")
        self.assertEqual(len(buddhist_list), 1)
        self.assertEqual(buddhist_list[0].id, "b1")

        search_res = self.repo.search_by_keyword("thời sự")
        self.assertEqual(len(search_res), 1)
        self.assertEqual(search_res[0].id, "n1")

    def test_viewing_history_recording(self):
        record = ViewingHistoryRecord(
            content_id="b1",
            title="Kinh Dược Sư",
            category="BUDDHIST",
            source=EventSource.VOICE_ASSISTANT,
            raw_utterance="Cháu bật kinh Dược Sư cho bà"
        )
        rec_id = self.repo.record_event(record)
        self.assertGreater(rec_id, 0)

        last = self.repo.get_last_played()
        self.assertIsNotNone(last)
        self.assertEqual(last.content_id, "b1")
        self.assertEqual(last.title, "Kinh Dược Sư")
        self.assertEqual(last.source, EventSource.VOICE_ASSISTANT)

    def test_preference_learning_heuristics(self):
        learner = LearnPreferencesUseCase(self.repo, self.repo)
        user = "grandmother"

        # 1. Yêu cầu chủ động (+3.0)
        learner.on_explicit_request(user, "buddhist_001", "BUDDHIST")
        scores = self.repo.get_preference_scores(user)
        self.assertEqual(scores.get("buddhist_001"), 53.0)
        self.assertEqual(scores.get("BUDDHIST"), 51.5)

        # 2. Bỏ qua ngay (-2.0)
        learner.on_immediate_skip(user, "buddhist_001")
        scores = self.repo.get_preference_scores(user)
        self.assertEqual(scores.get("buddhist_001"), 51.0)


if __name__ == "__main__":
    unittest.main()

