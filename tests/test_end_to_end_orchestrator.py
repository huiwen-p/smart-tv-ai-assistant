import unittest
import os
import sys
import tempfile
from typing import List, Tuple, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities.content_item import ContentItem, LaunchStrategy
from domain.entities.intent import TVActionType, ResolvedCommand
from domain.entities.conversation_state import ConversationState, DialogueState
from domain.entities.viewing_history import ViewingHistoryRecord, EventSource
from application.ports.device_port import DeviceControllerPort
from application.ports.voice_port import VoiceFeedbackPort
from application.ports.ai_resolver_port import BaseAIResolverPort
from application.use_cases.retrieve_candidates import RetrieveCandidatesUseCase
from application.use_cases.resolve_user_intent import ResolveUserIntentUseCase
from application.use_cases.plan_action import PlanActionUseCase
from application.use_cases.learn_preferences import LearnPreferencesUseCase
from application.use_cases.tv_state_verifier import TVStateVerifier
from application.use_cases.process_voice_command import ProcessVoiceCommandUseCase
from infrastructure.persistence.sqlite_repository_adapter import SqliteRepositoryAdapter
from infrastructure.ai.hybrid_resolver_adapter import HybridAIResolverAdapter


class MockDeviceAdapter(DeviceControllerPort):
    def __init__(self):
        self.keys_sent = []
        self.links_opened = []
        self.connected = True
        self.current_focus = "com.google.android.youtube.tv"

    def is_connected(self) -> bool:
        return self.connected

    def send_key(self, key_code: str, repeat: int = 1) -> bool:
        self.keys_sent.append((key_code, repeat))
        return True

    def open_deeplink(self, uri: str) -> Tuple[bool, str]:
        self.links_opened.append(uri)
        return True, f"Opened {uri}"

    def launch_app(self, packages: List[str]) -> Tuple[bool, str]:
        return True, "App launched"

    def search_youtube(self, query: str) -> Tuple[bool, str]:
        return True, f"Searched {query}"

    def open_vtv_channel(self, channel_code: str = "vtv1") -> Tuple[bool, str]:
        return True, f"Opened {channel_code}"

    def get_current_focus(self) -> Optional[str]:
        return self.current_focus


class MockVoiceAdapter(VoiceFeedbackPort):
    def __init__(self):
        self.spoken = []

    def speak(self, text: str):
        self.spoken.append(text)

    def play_ding(self):
        pass


class TestEndToEndOrchestrator(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite")
        self.temp_db.close()
        self.sqlite = SqliteRepositoryAdapter(self.temp_db.name)

        # Seed content
        self.sqlite.save(ContentItem(
            id="adida", name="Kinh A Di Đà", category="BUDDHIST", provider="YOUTUBE",
            launch_strategy=LaunchStrategy.DIRECT_DEEPLINK, deep_link="vnd.youtube://adida",
            speaker_or_artist="Thầy Thích Trí Thoát", tags=["kinh a di da"], default_priority=95
        ))
        self.sqlite.save(ContentItem(
            id="phaphoa", name="Kinh Pháp Hoa", category="BUDDHIST", provider="YOUTUBE",
            launch_strategy=LaunchStrategy.DIRECT_DEEPLINK, deep_link="vnd.youtube://phaphoa",
            speaker_or_artist="Thầy Thích Trí Thoát", tags=["kinh phap hoa"], default_priority=90
        ))

        self.device = MockDeviceAdapter()
        self.voice = MockVoiceAdapter()
        self.state = ConversationState()

        self.retriever = RetrieveCandidatesUseCase(self.sqlite, self.sqlite, self.sqlite)
        self.ai_resolver = HybridAIResolverAdapter()
        self.resolver = ResolveUserIntentUseCase(self.ai_resolver)
        self.planner = PlanActionUseCase()
        self.learning = LearnPreferencesUseCase(self.sqlite, self.sqlite)
        self.verifier = TVStateVerifier(self.device)

        self.orchestrator = ProcessVoiceCommandUseCase(
            retriever=self.retriever,
            resolver=self.resolver,
            planner=self.planner,
            learning=self.learning,
            verifier=self.verifier,
            device=self.device,
            voice=self.voice,
            history_repo=self.sqlite,
            content_repo=self.sqlite,
            state=self.state
        )

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            try:
                os.remove(self.temp_db.name)
            except Exception:
                pass

    def test_fastpath_volume_up_execution(self):
        result = self.orchestrator.execute("to tiếng lên")
        self.assertTrue(result.success)
        self.assertIn(("KEYCODE_VOLUME_UP", 3), self.device.keys_sent)
        self.assertTrue(any("tăng âm lượng" in s for s in self.voice.spoken))

    def test_vtv1_execution_and_history_logging(self):
        result = self.orchestrator.execute("bật vtv1")
        self.assertTrue(result.success)
        history = self.sqlite.get_recent_history()
        self.assertGreater(len(history), 0)
        self.assertIn("VTV1", history[0].title)

    def test_curated_buddhist_content_selection(self):
        result = self.orchestrator.execute("Cháu bật kinh A Di Đà cho bà nghe")
        self.assertTrue(result.success)
        self.assertIn("vnd.youtube://adida", self.device.links_opened)
        history = self.sqlite.get_recent_history()
        self.assertEqual(history[0].content_id, "adida")
        scores = self.sqlite.get_preference_scores()
        self.assertGreater(scores.get("adida", 50), 50)

    def test_multi_turn_clarification(self):
        # Thiết lập trạng thái đang chờ giải đáp giữa 2 bài
        self.state.dialogue_state = DialogueState.AWAITING_CLARIFICATION
        self.state.last_candidate_ids = ["adida", "phaphoa"]

        # Bà nói "cái thứ nhất"
        result = self.orchestrator.execute("cái thứ nhất")
        self.assertTrue(result.success)
        self.assertIn("vnd.youtube://adida", self.device.links_opened)
        self.assertEqual(self.state.dialogue_state, DialogueState.EXECUTING)


if __name__ == "__main__":
    unittest.main()

