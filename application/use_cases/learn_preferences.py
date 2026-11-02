from domain.entities.viewing_history import ViewingHistoryRecord, CompletionStatus, EventSource
from application.ports.repository_ports import PreferenceRepositoryPort, HistoryRepositoryPort


class LearnPreferencesUseCase:
    """
    Preference Learning Engine (Quy tắc Heuristic):
    Cập nhật điểm ưu tiên theo hành vi thực tế của người dùng:
    - Chủ động yêu cầu: +3.0
    - Nghe trọn vẹn: +2.0
    - Bỏ qua / đổi bài ngay (<30s): -2.0
    - Phản hồi tiêu cực ("không phải bài này"): -3.0
    """

    def __init__(
        self,
        preference_repo: PreferenceRepositoryPort,
        history_repo: HistoryRepositoryPort
    ):
        self.preference_repo = preference_repo
        self.history_repo = history_repo

    def on_explicit_request(self, user_id: str, content_id: str, category: str):
        """Khi người dùng chủ động yêu cầu đích danh nội dung."""
        self.preference_repo.update_preference_score(user_id, content_id, "CONTENT", 3.0)
        self.preference_repo.update_preference_score(user_id, category, "CATEGORY", 1.5)

    def on_playback_completed(self, user_id: str, content_id: str, duration: int):
        """Khi người dùng nghe trọn vẹn nội dung."""
        self.preference_repo.update_preference_score(user_id, content_id, "CONTENT", 2.0)

    def on_immediate_skip(self, user_id: str, content_id: str):
        """Khi người dùng bấm đổi bài hoặc tắt ngay trong vòng 30 giây đầu."""
        self.preference_repo.update_preference_score(user_id, content_id, "CONTENT", -2.0)

    def on_negative_correction(self, user_id: str, content_id: str):
        """Khi người dùng nói câu hiệu chỉnh: 'Không phải bài này'."""
        self.preference_repo.update_preference_score(user_id, content_id, "CONTENT", -3.0)

