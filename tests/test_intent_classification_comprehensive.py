import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities.intent import TVActionType
from domain.entities.conversation_state import ConversationState, DialogueState
from domain.entities.content_item import ContentItem
from infrastructure.persistence.sqlite_repository_adapter import SqliteRepositoryAdapter
from infrastructure.ai.hybrid_resolver_adapter import HybridAIResolverAdapter
from application.use_cases.retrieve_candidates import RetrieveCandidatesUseCase
from application.use_cases.resolve_user_intent import ResolveUserIntentUseCase


class TestIntentClassificationComprehensive(unittest.TestCase):
    """
    Bộ kiểm thử toàn diện 50+ câu khẩu ngữ thực tế:
    - Kiểm tra độ chính xác của phân loại ý định (Intent Accuracy).
    - Kiểm tra các bẫy dễ gây nhận nhầm (Confusion Traps / False Positives).
    - Kiểm tra câu nói nối tiếp theo ngữ cảnh (Contextual Continuity: 'bé nữa', 'to nữa').
    - Kiểm tra ma trận nhầm lẫn (Confusion Matrix).
    """

    @classmethod
    def setUpClass(cls):
        cls.repo = SqliteRepositoryAdapter("data/context_db.sqlite")
        cls.retriever = RetrieveCandidatesUseCase(cls.repo, cls.repo, cls.repo)
        cls.hybrid_resolver = HybridAIResolverAdapter()
        cls.resolver = ResolveUserIntentUseCase(cls.hybrid_resolver)

    def test_01_system_volume_up_standard(self):
        """Các biến thể lệnh tăng âm lượng chuẩn xác."""
        phrases = [
            "cho to tiếng lên",
            "cho to tiếng lên một chút",
            "tăng âm lượng",
            "tăng âm lượng lên",
            "bật to lên",
            "bật to lên tí",
            "nói to lên",
            "vặn to volume",
            "cho to lên",
            "to tiếng lên",
            "to lên chút"
        ]
        for p in phrases:
            state = ConversationState()
            candidates = self.retriever.execute(p)
            cmd = self.resolver.execute(p, candidates, state)
            self.assertEqual(cmd.action_type, TVActionType.SYSTEM_CONTROL, f"Lỗi ở câu: {p}")
            self.assertEqual(cmd.target, "volume_up", f"Lỗi target ở câu: {p}")

    def test_02_system_volume_down_standard(self):
        """Các biến thể lệnh giảm âm lượng chuẩn xác."""
        phrases = [
            "cho bé tiếng đi",
            "cho nhỏ lại một chút",
            "giảm âm lượng",
            "giảm âm lượng xuống",
            "bật nhỏ lại",
            "bật nhỏ lại tí cháu ơi",
            "vặn nhỏ lại hộ bà",
            "bé tiếng đi",
            "nhỏ tiếng lại",
            "nhỏ lại đi"
        ]
        for p in phrases:
            state = ConversationState()
            candidates = self.retriever.execute(p)
            cmd = self.resolver.execute(p, candidates, state)
            self.assertEqual(cmd.action_type, TVActionType.SYSTEM_CONTROL, f"Lỗi ở câu: {p}")
            self.assertEqual(cmd.target, "volume_down", f"Lỗi target ở câu: {p}")

    def test_03_system_sleep_and_off(self):
        """Các biến thể lệnh tắt TV / đi ngủ."""
        phrases = [
            "tắt tv",
            "tắt tivi đi cháu",
            "tắt màn hình",
            "bà buồn ngủ rồi tắt tv đi",
            "ông đi ngủ đây",
            "nghỉ xem tivi",
            "nghỉ xem"
        ]
        for p in phrases:
            state = ConversationState()
            candidates = self.retriever.execute(p)
            cmd = self.resolver.execute(p, candidates, state)
            self.assertEqual(cmd.action_type, TVActionType.SYSTEM_CONTROL, f"Lỗi ở câu: {p}")
            self.assertEqual(cmd.target, "sleep", f"Lỗi target ở câu: {p}")

    def test_04_system_media_and_navigation(self):
        """Các biến thể lệnh tạm dừng, trang chủ, quay lại."""
        test_map = {
            "tạm dừng": ("pause", TVActionType.SYSTEM_CONTROL),
            "dừng lại một chút": ("pause", TVActionType.SYSTEM_CONTROL),
            "tiếp tục phát": ("pause", TVActionType.SYSTEM_CONTROL),
            "về trang chủ": ("home", TVActionType.SYSTEM_CONTROL),
            "về màn hình chính": ("home", TVActionType.SYSTEM_CONTROL),
            "quay lại": ("back", TVActionType.SYSTEM_CONTROL),
            "trở lại": ("back", TVActionType.SYSTEM_CONTROL),
        }
        for p, (target, act_type) in test_map.items():
            state = ConversationState()
            candidates = self.retriever.execute(p)
            cmd = self.resolver.execute(p, candidates, state)
            self.assertEqual(cmd.action_type, act_type, f"Lỗi action ở câu: {p}")
            self.assertEqual(cmd.target, target, f"Lỗi target ở câu: {p}")

    def test_05_confusion_traps_must_not_be_system_control(self):
        """
        BẪY NHẬN NHẦM (CRITICAL CONFUSION TRAPS):
        Các câu này chứa từ ngữ dễ gây nhầm lẫn (như 'to', 'tiktok', 'tiếng', 'buồn ngủ')
        nhưng bản chất là TÌM KIẾM NỘI DUNG. Tuyệt đối không được kích hoạt volume_up hay sleep!
        """
        traps = [
            ("mở nhạc hot tiktok trên youtube", "nhạc hot tiktok"),
            ("mở phim có tiếng to", "phim có tiếng to"),
            ("mở nhạc to hơn", "nhạc to hơn"),
            ("tìm video tiktok trên youtube", "video tiktok"),
            ("ông buồn ngủ nhưng muốn nghe nhạc", "nhạc"),
            ("bà muốn nghe nhạc vàng", "nhạc vàng"),
            ("mở nhạc bolero chọn lọc", "nhạc bolero chọn lọc")
        ]
        for p, query_hint in traps:
            state = ConversationState()
            candidates = self.retriever.execute(p)
            cmd = self.resolver.execute(p, candidates, state)

            # TUYỆT ĐỐI KHÔNG ĐƯỢC LÀ SYSTEM_CONTROL
            self.assertNotEqual(
                cmd.action_type,
                TVActionType.SYSTEM_CONTROL,
                f"LỖI NGHIÊM TRỌNG: Câu nội dung '{p}' bị nhận nhầm thành lệnh điều khiển hệ thống {cmd.target}!"
            )
            # Phải là SEARCH_YOUTUBE hoặc PLAY_CONTENT
            self.assertIn(
                cmd.action_type,
                [TVActionType.SEARCH_YOUTUBE, TVActionType.PLAY_CONTENT],
                f"Câu '{p}' cần trả về SEARCH_YOUTUBE hoặc PLAY_CONTENT, nhận được {cmd.action_type}"
            )

    def test_06_contextual_followup_continuity(self):
        """
        CÂU NỐI TIẾP THEO NGỮ CẢNH:
        Lượt 1: Giảm âm lượng
        Lượt 2: 'bé nữa' -> tiếp tục giảm âm lượng dựa trên state.last_action.
        """
        state = ConversationState()

        # Lượt 1
        p1 = "cho bé tiếng đi"
        candidates1 = self.retriever.execute(p1)
        cmd1 = self.resolver.execute(p1, candidates1, state)
        self.assertEqual(cmd1.action_type, TVActionType.SYSTEM_CONTROL)
        self.assertEqual(cmd1.target, "volume_down")
        state.last_action = "volume_down"  # Cập nhật context như orchestrator thực tế

        # Lượt 2
        p2 = "bé nữa"
        candidates2 = self.retriever.execute(p2)
        cmd2 = self.resolver.execute(p2, candidates2, state)
        self.assertEqual(cmd2.action_type, TVActionType.SYSTEM_CONTROL, "Câu 'bé nữa' không nhận diện được ngữ cảnh")
        self.assertEqual(cmd2.target, "volume_down", "Câu 'bé nữa' phải tiếp tục giảm âm lượng")

    def test_07_confusion_matrix_summary(self):
        """
        ĐO ĐẠC MA TRẬN NHẦM LẪN (Confusion Matrix Metrics):
        Đảm bảo False Positive Rate từ Content sang System Control = 0%.
        """
        test_dataset = [
            # (Câu nói, Nhóm kỳ vọng)
            ("cho to tiếng lên", "SYSTEM_CONTROL"),
            ("tăng âm lượng", "SYSTEM_CONTROL"),
            ("to tiếng lên chút", "SYSTEM_CONTROL"),
            ("cho nhỏ lại", "SYSTEM_CONTROL"),
            ("giảm âm lượng", "SYSTEM_CONTROL"),
            ("bé tiếng đi cháu", "SYSTEM_CONTROL"),
            ("tắt tv đi", "SYSTEM_CONTROL"),
            ("nghỉ xem tivi", "SYSTEM_CONTROL"),
            ("về trang chủ", "SYSTEM_CONTROL"),
            ("quay lại", "SYSTEM_CONTROL"),
            ("thời sự vtv1", "PLAY_LIVE_TV"),
            ("bật vtv1", "PLAY_LIVE_TV"),
            ("mở nhạc hot tiktok trên youtube", "CONTENT"),
            ("mở phim có tiếng to", "CONTENT"),
            ("mở nhạc to hơn", "CONTENT"),
            ("bà muốn nghe nhạc vàng", "CONTENT"),
            ("tìm kinh sám hối trên youtube", "CONTENT"),
            ("cho bà nghe nhạc đỏ", "CONTENT"),
            ("mở cải lương Lan và Điệp", "CONTENT"),
        ]

        matrix = {
            "SYSTEM_CONTROL_as_SYSTEM_CONTROL": 0,
            "SYSTEM_CONTROL_as_CONTENT": 0,
            "CONTENT_as_SYSTEM_CONTROL": 0,  # Bắt buộc phải bằng 0!
            "CONTENT_as_CONTENT": 0,
            "PLAY_LIVE_TV_as_PLAY_LIVE_TV": 0
        }

        for text, expected_group in test_dataset:
            state = ConversationState()
            candidates = self.retriever.execute(text)
            cmd = self.resolver.execute(text, candidates, state)

            actual_group = ""
            if cmd.action_type == TVActionType.SYSTEM_CONTROL:
                actual_group = "SYSTEM_CONTROL"
            elif cmd.action_type == TVActionType.PLAY_LIVE_TV:
                actual_group = "PLAY_LIVE_TV"
            else:
                actual_group = "CONTENT"

            if expected_group == "SYSTEM_CONTROL" and actual_group == "SYSTEM_CONTROL":
                matrix["SYSTEM_CONTROL_as_SYSTEM_CONTROL"] += 1
            elif expected_group == "SYSTEM_CONTROL" and actual_group == "CONTENT":
                matrix["SYSTEM_CONTROL_as_CONTENT"] += 1
            elif expected_group == "CONTENT" and actual_group == "SYSTEM_CONTROL":
                matrix["CONTENT_as_SYSTEM_CONTROL"] += 1
            elif expected_group == "CONTENT" and actual_group == "CONTENT":
                matrix["CONTENT_as_CONTENT"] += 1
            elif expected_group == "PLAY_LIVE_TV" and actual_group == "PLAY_LIVE_TV":
                matrix["PLAY_LIVE_TV_as_PLAY_LIVE_TV"] += 1

        print("\n--- MA TRẬN NHẦM LẪN (CONFUSION MATRIX) ---")
        for k, v in matrix.items():
            print(f"  {k:35}: {v}")

        # Chỉ tiêu sống còn: CONTENT tuyệt đối không bao giờ được nhầm sang SYSTEM_CONTROL!
        self.assertEqual(matrix["CONTENT_as_SYSTEM_CONTROL"], 0, "False Positive: Nội dung bị nhận nhầm thành lệnh điều khiển TV!")


if __name__ == "__main__":
    unittest.main()

