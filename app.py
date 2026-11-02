import sys
import os

# Đảm bảo import được các module từ thư mục gốc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from domain.entities.intent import TVActionType, ResolvedCommand, ExecutionResult
from domain.entities.conversation_state import ConversationState

# Ports & Use Cases (Application Layer)
from application.use_cases.retrieve_candidates import RetrieveCandidatesUseCase
from application.use_cases.resolve_user_intent import ResolveUserIntentUseCase
from application.use_cases.plan_action import PlanActionUseCase
from application.use_cases.learn_preferences import LearnPreferencesUseCase
from application.use_cases.tv_state_verifier import TVStateVerifier
from application.use_cases.process_voice_command import ProcessVoiceCommandUseCase

# Adapters (Infrastructure Layer)
from infrastructure.persistence.sqlite_repository_adapter import SqliteRepositoryAdapter
from infrastructure.ai.hybrid_resolver_adapter import HybridAIResolverAdapter
from infrastructure.device.closed_loop_adb_adapter import ClosedLoopAdbAdapter
from infrastructure.voice.edge_tts_adapter import EdgeTtsAdapter
from infrastructure.input.cli_adapter import CliInputAdapter


class VoiceTVAssistantApp:
    """
    Ứng dụng chính (Orchestrator):
    Tuân thủ Clean Architecture - nhận Orchestrator Use Case thông qua Dependency Injection.
    """

    def __init__(
        self,
        process_use_case: ProcessVoiceCommandUseCase,
        input_source: CliInputAdapter,
        device: ClosedLoopAdbAdapter
    ):
        self.process_use_case = process_use_case
        self.input = input_source
        self.device = device

    def print_welcome(self):
        print("=" * 72)
        print("   TRỢ LÝ TV THÔNG MINH HIỂU NGỮ CẢNH (CONTEXT-AWARE CONVERSATIONAL AI)   ")
        print("=" * 72)
        connected = self.device.is_connected()
        status_icon = "✓" if connected else "!"
        device_id = getattr(self.device, "active_device", "")
        device_label = f" ({device_id})" if device_id else ""
        print(f"[{status_icon}] Trạng thái TV Xiaomi: {'ĐÃ KẾT NỐI' + device_label if connected else 'CHƯA TÌM THẤY'}")
        if not connected:
            print("    -> Gợi ý kết nối:")
            print("       1. Chạy lệnh: 'connect <IP>' (ví dụ: connect 10.88.88.163)")
            print("       2. Hoặc cắm cáp USB một lần, chạy 'adb tcpip 5555' rồi rút cáp.")
        print("-" * 72)
        print("✨ Bây giờ bạn có thể nói/gõ BẤT KỲ CÂU GÌ một cách tự nhiên theo khẩu ngữ ông bà:")
        print("  - 'Cháu bật bài kinh cho bà nghe'")
        print("  - 'Mở cái hôm qua bà nghe ấy'")
        print("  - 'Bật thời sự đi cháu'")
        print("  - 'Mở nhạc vàng Chế Linh'")
        print("  - 'Nói to lên cháu ơi'")
        print("  - 'Bà buồn ngủ rồi tắt TV đi'")
        print("  - Gõ 'exit' để thoát.")
        print("=" * 72)

    def run(self):
        self.print_welcome()
        while True:
            raw_command = self.input.wait_for_trigger()
            if raw_command is None or raw_command.lower() in ["exit", "thoat", "quit"]:
                print("\nĐã dừng chương trình. Chúc ông bà một ngày an vui!")
                break

            if not raw_command.strip():
                continue

            cmd_lower = raw_command.strip().lower()

            # Lệnh tiện ích kết nối adb
            if cmd_lower.startswith("connect ") or cmd_lower.startswith("ket noi "):
                ip_arg = raw_command.strip().split(maxsplit=1)[1]
                if hasattr(self.device, "target_ip"):
                    self.device.target_ip = ip_arg
                    self.device._connect_wifi()
                    if self.device.is_connected():
                        print(f"[✓] Đã kết nối thành công tới thiết bị: {self.device.active_device}")
                    else:
                        print(f"[!] Không thể kết nối tới {ip_arg}.")
                continue

            # Thực thi qua Use Case tổng
            result = self.process_use_case.execute(raw_command)
            status_char = "✓" if result.success else "✗"
            print(f"[{status_char}] {result.message}")


def main():
    # 1. Khởi tạo Cơ sở dữ liệu Ngữ cảnh SQLite
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "context_db.sqlite")
    sqlite_adapter = SqliteRepositoryAdapter(db_path)

    # 2. Khởi tạo Adapters Hạ tầng
    ai_resolver = HybridAIResolverAdapter()
    device_adapter = ClosedLoopAdbAdapter()
    voice_adapter = EdgeTtsAdapter()
    input_adapter = CliInputAdapter()

    # 3. Khởi tạo các Use Cases theo Clean Architecture
    conv_state = ConversationState()
    retriever = RetrieveCandidatesUseCase(
        content_repo=sqlite_adapter,
        history_repo=sqlite_adapter,
        preference_repo=sqlite_adapter
    )
    resolver = ResolveUserIntentUseCase(ai_resolver=ai_resolver)
    planner = PlanActionUseCase()
    learning = LearnPreferencesUseCase(
        preference_repo=sqlite_adapter,
        history_repo=sqlite_adapter
    )
    verifier = TVStateVerifier(device=device_adapter)

    process_use_case = ProcessVoiceCommandUseCase(
        retriever=retriever,
        resolver=resolver,
        planner=planner,
        learning=learning,
        verifier=verifier,
        device=device_adapter,
        voice=voice_adapter,
        history_repo=sqlite_adapter,
        content_repo=sqlite_adapter,
        state=conv_state
    )

    # 4. Chạy ứng dụng
    app = VoiceTVAssistantApp(
        process_use_case=process_use_case,
        input_source=input_adapter,
        device=device_adapter
    )
    app.run()


if __name__ == "__main__":
    main()
