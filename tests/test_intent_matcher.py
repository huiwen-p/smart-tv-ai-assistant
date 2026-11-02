import unittest
import os
import sys

# Thêm thư mục gốc vào path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities.intent import TVActionType
from infrastructure.ai.hybrid_resolver_adapter import HybridAIResolverAdapter


class TestIntentMatcher(unittest.TestCase):
    """
    Kiểm thử bộ so khớp ý định tức thì Fast-Path (0ms Offline)
    dành cho các câu lệnh khẩu ngữ phổ biến của người cao tuổi.
    """
    @classmethod
    def setUpClass(cls):
        cls.resolver = HybridAIResolverAdapter()

    def test_watch_vtv1_match(self):
        queries = [
            "bật vtv1",
            "cho ông xem thời sự",
            "đến giờ thời sự rồi",
            "xem thời sự",
            "bật thời sự",
            "mở vtv1"
        ]
        for q in queries:
            cmd = self.resolver.resolve(q)
            self.assertEqual(cmd.action_type, TVActionType.PLAY_LIVE_TV, f"Không khớp đúng action: {q}")
            self.assertEqual(cmd.target, "vtv1", f"Không khớp kênh vtv1: {q}")
            self.assertEqual(cmd.confidence, 1.0)

    def test_volume_control_match(self):
        up_queries = ["nói to lên", "to lên", "bật to lên", "tăng âm lượng", "to tiếng lên"]
        for q in up_queries:
            cmd = self.resolver.resolve(q)
            self.assertEqual(cmd.action_type, TVActionType.SYSTEM_CONTROL)
            self.assertEqual(cmd.target, "volume_up")
            self.assertEqual(cmd.confidence, 1.0)

        down_queries = ["nhỏ lại", "bật nhỏ lại", "giảm âm lượng", "bé lại", "nhỏ tiếng"]
        for q in down_queries:
            cmd = self.resolver.resolve(q)
            self.assertEqual(cmd.action_type, TVActionType.SYSTEM_CONTROL)
            self.assertEqual(cmd.target, "volume_down")
            self.assertEqual(cmd.confidence, 1.0)

    def test_sleep_and_turn_off_match(self):
        queries = ["tắt tv", "đi ngủ", "ông đi ngủ đây", "bà đi ngủ đây", "nghỉ xem"]
        for q in queries:
            cmd = self.resolver.resolve(q)
            self.assertEqual(cmd.action_type, TVActionType.SYSTEM_CONTROL)
            self.assertEqual(cmd.target, "sleep")
            self.assertEqual(cmd.confidence, 1.0)

    def test_navigation_and_playback_control(self):
        pause_queries = ["tạm dừng", "dừng lại", "tiếp tục", "phát tiếp"]
        for q in pause_queries:
            cmd = self.resolver.resolve(q)
            self.assertEqual(cmd.action_type, TVActionType.SYSTEM_CONTROL)
            self.assertEqual(cmd.target, "pause")

        home_queries = ["về trang chủ", "về màn hình chính", "màn hình chính"]
        for q in home_queries:
            cmd = self.resolver.resolve(q)
            self.assertEqual(cmd.action_type, TVActionType.SYSTEM_CONTROL)
            self.assertEqual(cmd.target, "home")


if __name__ == "__main__":
    unittest.main()
