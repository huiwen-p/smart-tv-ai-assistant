import os
from dataclasses import dataclass


@dataclass
class Settings:
    # 1. Cấu hình thiết bị đích (Android Phone hoặc TV Xiaomi)
    # - Nếu kết nối qua USB: để trống ""
    # - Nếu kết nối qua Wi-Fi: Có thể chỉ điền IP (ví dụ "10.88.88.163"), hệ thống sẽ tự động dò cổng (5555 / mDNS / quét cổng).
    #   Hoặc điền đầy đủ cả IP:PORT nếu muốn cố định (ví dụ "10.88.88.163:46849" hoặc "192.168.1.50:5555").
    TARGET_DEVICE_IP: str = os.getenv("TARGET_DEVICE_IP", "10.88.88.163")
    
    # 2. Cấu hình AI LLM (Gemini Flash Intent Resolver)
    GEMINI_API_KEY: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    USE_AI_RESOLVER: bool = True
    
    # 3. Đường dẫn file adb.exe dự phòng nếu chưa có trong PATH
    FALLBACK_ADB_PATH: str = r"D:\android-sdk\platform-tools\adb.exe"

    # 4. Đường dẫn file cấu hình quy tắc
    COMMANDS_CONFIG_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config",
        "commands.json"
    )

    # 5. Giọng đọc tiếng Việt (Microsoft Edge-TTS)
    TTS_VOICE: str = "vi-VN-HoaiMyNeural"  # Giọng nữ Bắc ấm áp hoặc "vi-VN-NamMinhNeural"
    TTS_RATE: str = "-10%"                # Đọc chậm hơn 10% cho người già dễ nghe

    # 6. Cấu hình Raspberry Pi GPIO (sử dụng khi lên phần cứng)
    GPIO_BUTTON_PIN: int = int(os.getenv("GPIO_BUTTON_PIN", "18"))
    GPIO_LED_GREEN: int = int(os.getenv("GPIO_LED_GREEN", "23"))
    GPIO_LED_RED: int = int(os.getenv("GPIO_LED_RED", "24"))

    # 7. Đường dẫn CSDL SQLite cục bộ
    DB_PATH: str = os.getenv(
        "DB_PATH",
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "context_db.sqlite")
    )


settings = Settings()

