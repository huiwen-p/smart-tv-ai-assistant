from abc import ABC, abstractmethod


class VoiceFeedbackPort(ABC):
    """Cổng giao tiếp phát âm thanh phản hồi (TTS) cho người cao tuổi."""

    @abstractmethod
    def speak(self, text: str):
        """Phát câu nói thưa gửi kính cẩn qua loa."""
        pass

    @abstractmethod
    def play_ding(self):
        """Phát âm báo 'Ting' tức thì khi bắt đầu/kết thúc nhận lệnh."""
        pass

