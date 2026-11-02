from typing import Optional
from application.ports.input_port import InputTriggerPort


class CliInputAdapter(InputTriggerPort):
    """
    Adapter nhập lệnh trực tiếp qua Terminal (dùng để phát triển và kiểm thử trên PC).
    """

    def wait_for_trigger(self) -> Optional[str]:
        try:
            cmd = input("\n[Bạn nói (hoặc gõ câu khẩu ngữ)] > ").strip()
            return cmd if cmd else None
        except (KeyboardInterrupt, EOFError):
            return "exit"

    def listen_for_command(self) -> Optional[str]:
        return self.wait_for_trigger()
