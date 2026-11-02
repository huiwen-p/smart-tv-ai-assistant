import time
from typing import Optional
from domain.entities.intent import TVActionType, ResolvedCommand, ExecutionResult
from domain.entities.conversation_state import ConversationState, DialogueState
from domain.entities.viewing_history import ViewingHistoryRecord, EventSource, CompletionStatus
from application.ports.device_port import DeviceControllerPort
from application.ports.voice_port import VoiceFeedbackPort
from application.ports.repository_ports import (
    ContentRepositoryPort,
    HistoryRepositoryPort,
    PreferenceRepositoryPort
)
from application.use_cases.retrieve_candidates import RetrieveCandidatesUseCase
from application.use_cases.resolve_user_intent import ResolveUserIntentUseCase
from application.use_cases.plan_action import PlanActionUseCase
from application.use_cases.learn_preferences import LearnPreferencesUseCase
from application.use_cases.tv_state_verifier import TVStateVerifier


class ProcessVoiceCommandUseCase:
    """
    Orchestrator Use Case:
    Điều phối toàn bộ chu trình xử lý khẩu ngữ của ông bà theo Clean Architecture:
    1. Nhận chuỗi văn bản khẩu ngữ.
    2. Candidate Retrieval truy xuất 3-5 nội dung từ Catalog & History.
    3. Phân loại ý định 3 trạng thái (Resolve Intent).
    4. Kế hoạch hành động & Policy Gate (Plan Action).
    5. Điều khiển thiết bị và xác minh vòng lặp đóng (Execute & Verify).
    6. Ghi nhận lịch sử và học sở thích.
    7. Phản hồi giọng nói thưa gửi kính cẩn qua TTS.
    """

    def __init__(
        self,
        retriever: RetrieveCandidatesUseCase,
        resolver: ResolveUserIntentUseCase,
        planner: PlanActionUseCase,
        learning: LearnPreferencesUseCase,
        verifier: TVStateVerifier,
        device: DeviceControllerPort,
        voice: VoiceFeedbackPort,
        history_repo: HistoryRepositoryPort,
        content_repo: ContentRepositoryPort,
        state: Optional[ConversationState] = None
    ):
        self.retriever = retriever
        self.resolver = resolver
        self.planner = planner
        self.learning = learning
        self.verifier = verifier
        self.device = device
        self.voice = voice
        self.history_repo = history_repo
        self.content_repo = content_repo
        self.state = state or ConversationState()

    def execute(self, user_utterance: str) -> ExecutionResult:
        if not user_utterance or not user_utterance.strip():
            return ExecutionResult(False, "Câu lệnh rỗng")

        # Kiểm tra session hết hạn
        if self.state.is_expired():
            self.state.reset()

        # 1. Candidate Retrieval: Lấy 3-5 ứng viên tiềm năng
        candidates = self.retriever.execute(
            query_text=user_utterance,
            temporal_reference=user_utterance if any(w in user_utterance.lower() for w in ["hôm qua", "vừa rồi", "sáng nay"]) else None
        )

        # 2. Phân loại ý định 3 trạng thái
        cmd: ResolvedCommand = self.resolver.execute(user_utterance, candidates, self.state)

        # 3. Kế hoạch hành động & Policy Gate
        content_item = self.content_repo.get_by_id(cmd.content_id) if cmd.content_id else None
        cmd = self.planner.execute(cmd, content_item)

        # 4. Phát phản hồi giọng nói thưa gửi (nếu có câu chào)
        if cmd.feedback:
            self.voice.speak(cmd.feedback)

        # 5. Nếu là trạng thái hỏi lại (CLARIFY), không điều khiển TV
        if cmd.action_type == TVActionType.CLARIFY:
            return ExecutionResult(True, "Đang hỏi lại làm rõ", cmd.feedback)

        # 6. Điều khiển TV
        exec_ok = False
        msg = ""

        if cmd.action_type == TVActionType.PLAY_LIVE_TV:
            ch = cmd.target or "vtv1"
            exec_ok, msg = self.device.open_vtv_channel(ch)
            if exec_ok:
                self.history_repo.record_event(ViewingHistoryRecord(
                    title=f"Kênh thời sự {ch.upper()}",
                    category="NEWS",
                    source=EventSource.VOICE_ASSISTANT,
                    raw_utterance=user_utterance
                ))

        elif cmd.action_type == TVActionType.PLAY_CONTENT:
            target_link = cmd.target or (content_item.deep_link if content_item else "")
            exec_ok, msg = self.device.open_deeplink(target_link)
            if exec_ok and content_item:
                self.history_repo.record_event(ViewingHistoryRecord(
                    content_id=content_item.id,
                    title=content_item.name,
                    category=content_item.category,
                    source=EventSource.VOICE_ASSISTANT,
                    raw_utterance=user_utterance
                ))
                self.learning.on_explicit_request("grandmother", content_item.id, content_item.category)
                self.state.currently_playing_id = content_item.id

        elif cmd.action_type == TVActionType.SEARCH_YOUTUBE:
            query = cmd.query or user_utterance
            exec_ok, msg = self.device.search_youtube(query)

        elif cmd.action_type == TVActionType.SYSTEM_CONTROL:
            self.state.last_action = cmd.target
            self.state.touch()
            key_map = {
                "volume_up": ("KEYCODE_VOLUME_UP", 3),
                "volume_down": ("KEYCODE_VOLUME_DOWN", 3),
                "sleep": ("KEYCODE_SLEEP", 1),
                "pause": ("KEYCODE_MEDIA_PLAY_PAUSE", 1),
                "home": ("KEYCODE_HOME", 1),
                "back": ("KEYCODE_BACK", 1)
            }
            if cmd.target in key_map:
                k, r = key_map[cmd.target]
                exec_ok = self.device.send_key(k, r)
                msg = f"Đã gửi {k}"
            else:
                exec_ok = self.device.send_key(cmd.target, 1)
                msg = f"Đã gửi {cmd.target}"

        elif cmd.action_type == TVActionType.OPEN_APP:
            exec_ok, msg = self.device.launch_app([cmd.target])

        else:
            exec_ok = False
            msg = "Chưa nhận diện được hành động"

        return ExecutionResult(exec_ok, msg, cmd.feedback)

