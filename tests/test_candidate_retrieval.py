import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities.content_item import ContentItem
from domain.entities.viewing_history import ViewingHistoryRecord, EventSource
from infrastructure.persistence.sqlite_repository_adapter import SqliteRepositoryAdapter
from application.use_cases.retrieve_candidates import RetrieveCandidatesUseCase


class TestCandidateRetrieval(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite")
        self.temp_db.close()
        self.repo = SqliteRepositoryAdapter(self.temp_db.name)
        self.retriever = RetrieveCandidatesUseCase(self.repo, self.repo, self.repo)

        # Seed một vài item mẫu
        self.repo.save(ContentItem(
            id="adida", name="Kinh A Di Đà", category="BUDDHIST", provider="YOUTUBE",
            speaker_or_artist="Thầy Thích Trí Thoát", tags=["kinh phat"], default_priority=95
        ))
        self.repo.save(ContentItem(
            id="phaphoa", name="Kinh Pháp Hoa", category="BUDDHIST", provider="YOUTUBE",
            speaker_or_artist="Thầy Thích Trí Thoát", tags=["kinh phat"], default_priority=90
        ))
        self.repo.save(ContentItem(
            id="vtv1", name="Thời sự VTV1", category="NEWS", provider="VTVGO",
            speaker_or_artist="VTV", tags=["thoi su"], default_priority=85
        ))

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            try:
                os.remove(self.temp_db.name)
            except Exception:
                pass

    def test_retrieve_by_keyword(self):
        candidates = self.retriever.execute(query_text="nghe kinh a di đà")
        self.assertGreater(len(candidates), 0)
        self.assertEqual(candidates[0].id, "adida")

    def test_retrieve_by_category_hint(self):
        candidates = self.retriever.execute(query_text="mở cái gì đó", category_hint="NEWS")
        self.assertGreater(len(candidates), 0)
        self.assertEqual(candidates[0].id, "vtv1")

    def test_retrieve_by_temporal_reference(self):
        # Giả lập lịch sử xem hôm qua
        self.repo.record_event(ViewingHistoryRecord(
            content_id="phaphoa",
            title="Kinh Pháp Hoa",
            category="BUDDHIST",
            source=EventSource.VOICE_ASSISTANT,
            raw_utterance="Mở kinh Pháp Hoa"
        ))

        candidates = self.retriever.execute(
            query_text="mở bài hôm qua bà nghe",
            temporal_reference="hôm qua"
        )
        self.assertGreater(len(candidates), 0)
        self.assertEqual(candidates[0].id, "phaphoa")


if __name__ == "__main__":
    unittest.main()

