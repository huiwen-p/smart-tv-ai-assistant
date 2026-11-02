from abc import ABC, abstractmethod
from typing import Optional


class InputTriggerPort(ABC):
    """Cổng nhận tín hiệu kích hoạt từ người dùng (Push-to-Talk / Bàn phím / CLI)."""

    @abstractmethod
    def wait_for_trigger(self) -> Optional[str]:
        """Chờ sự kiện bấm nút và trả về câu văn bản nhận diện được từ giọng nói."""
        pass

