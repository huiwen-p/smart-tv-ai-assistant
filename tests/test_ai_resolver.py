import unittest
import os
import sys

# Thêm thư mục gốc vào path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities.intent import TVActionType
from infrastructure.ai.hybrid_resolver_adapter import HybridAIResolverAdapter


class TestHybridAIResolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resolver = HybridAIResolverAdapter()

    def test_fastpath_volume_up(self):
        for q in ["tăng âm lượng", "cho to tiếng lên một chút", "bật to lên tí", "vặn to lên"]:
            res = self.resolver.resolve(q)
            self.assertEqual(res.action_type, TVActionType.SYSTEM_CONTROL, f"Failed for {q}")
            self.assertEqual(res.target, "volume_up", f"Failed for {q}")

    def test_fastpath_volume_down(self):
        for q in ["nhỏ tiếng", "cho nhỏ lại một chút", "vặn nhỏ lại hộ bà", "bé tiếng đi"]:
            res = self.resolver.resolve(q)
            self.assertEqual(res.action_type, TVActionType.SYSTEM_CONTROL, f"Failed for {q}")
            self.assertEqual(res.target, "volume_down", f"Failed for {q}")

    def test_fastpath_sleep(self):
        for q in ["ông đi ngủ đây", "bà buồn ngủ rồi tắt tv đi", "tắt tivi đi cháu"]:
            res = self.resolver.resolve(q)
            self.assertEqual(res.action_type, TVActionType.SYSTEM_CONTROL, f"Failed for {q}")
            self.assertEqual(res.target, "sleep", f"Failed for {q}")

    def test_fastpath_pause(self):
        res = self.resolver.resolve("tạm dừng")
        self.assertEqual(res.action_type, TVActionType.SYSTEM_CONTROL)
        self.assertEqual(res.target, "pause")

    def test_fastpath_vtv1(self):
        res = self.resolver.resolve("bật vtv1")
        self.assertEqual(res.action_type, TVActionType.PLAY_LIVE_TV)
        self.assertEqual(res.target, "vtv1")

    def test_fastpath_home_navigation(self):
        res = self.resolver.resolve("về trang chủ")
        self.assertEqual(res.action_type, TVActionType.SYSTEM_CONTROL)
        self.assertEqual(res.target, "home")


if __name__ == "__main__":
    unittest.main()
