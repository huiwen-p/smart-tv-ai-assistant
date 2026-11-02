from typing import Optional
from application.ports.device_port import DeviceControllerPort


class TVStateVerifier:
    """
    Closed-Loop TV State Verifier:
    Quan sát trạng thái màn hình TV sau khi gửi lệnh để xác minh lệnh đã thực thi đúng.
    """

    def __init__(self, device: DeviceControllerPort):
        self.device = device

    def verify_app_focused(self, expected_package_hint: str) -> bool:
        """Kiểm tra ứng dụng mục tiêu có đang chiếm màn hình TV không."""
        focus_info = self.device.get_current_focus()
        if not focus_info:
            return False
        return expected_package_hint.lower() in focus_info.lower()

