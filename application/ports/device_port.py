from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class DeviceControllerPort(ABC):
    """Cổng giao tiếp trừu tượng điều khiển thiết bị đích (Smart TV Xiaomi / Android)."""

    @abstractmethod
    def is_connected(self) -> bool:
        """Kiểm tra thiết bị có đang kết nối và sẵn sàng nhận lệnh không."""
        pass

    @abstractmethod
    def send_key(self, key_code: str, repeat: int = 1) -> bool:
        """Gửi mã phím hệ thống (Volume, Home, Back, Pause, Sleep...)."""
        pass

    @abstractmethod
    def open_deeplink(self, uri: str) -> Tuple[bool, str]:
        """Mở liên kết ứng dụng trực tiếp qua Android Intent."""
        pass

    @abstractmethod
    def launch_app(self, packages: List[str]) -> Tuple[bool, str]:
        """Khởi chạy ứng dụng từ danh sách package tiềm năng."""
        pass

    @abstractmethod
    def search_youtube(self, query: str) -> Tuple[bool, str]:
        """Mở YouTube và điền từ khóa tìm kiếm."""
        pass

    @abstractmethod
    def open_vtv_channel(self, channel_code: str = "vtv1") -> Tuple[bool, str]:
        """Mở kênh truyền hình VTV (VTVgo / Live Stream)."""
        pass

    @abstractmethod
    def get_current_focus(self) -> Optional[str]:
        """Lấy thông tin ứng dụng / cửa sổ đang chiếm màn hình TV (Closed-Loop Observation)."""
        pass

