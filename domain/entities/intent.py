from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any


class TVActionType(str, Enum):
    PLAY_LIVE_TV = "PLAY_LIVE_TV"        # vtv1, vtv2, vtv3
    PLAY_CONTENT = "PLAY_CONTENT"        # YouTube video / curated content
    SEARCH_YOUTUBE = "SEARCH_YOUTUBE"    # Tìm kiếm tự do khi không khớp catalog
    SYSTEM_CONTROL = "SYSTEM_CONTROL"    # volume_up, volume_down, sleep, pause, home, back
    CLARIFY = "CLARIFY"                  # Hỏi lại người dùng khi mơ hồ
    OPEN_APP = "OPEN_APP"                # Mở app theo tên (vtvgo, youtube)
    UNKNOWN = "UNKNOWN"


class IntentConfidence(str, Enum):
    HIGH = "HIGH"        # >= 0.85 -> Execute
    MEDIUM = "MEDIUM"    # 0.60 - 0.84 -> Clarify
    LOW = "LOW"          # < 0.60 -> Rephrase / Fallback


@dataclass
class ResolvedCommand:
    action_type: TVActionType
    target: str = ""                    # vtv1, volume_up, sleep, home...
    content_id: Optional[str] = None    # ID trong ContentCatalog
    query: str = ""                     # Từ khóa nếu cần tìm kiếm
    feedback: str = ""                  # Lời thưa gửi lễ phép: "Dạ, cháu đang bật..."
    confidence: float = 1.0
    raw_text: str = ""
    clarification_options: List[str] = field(default_factory=list)


@dataclass
class ExecutionResult:
    success: bool
    message: str
    feedback_text: str = ""

