from typing import Optional
from domain.entities.intent import TVActionType, ResolvedCommand
from domain.entities.conversation_state import ConversationState
from application.intent.system_command_patterns import (
    CONTENT_INTENT_PREFIX,
    CONTENT_INTENT_KEYWORD,
    NEGATION_PREFIX,
    VOLUME_UP_PATTERNS,
    VOLUME_DOWN_PATTERNS,
    FOLLOWUP_VOLUME_DOWN_PATTERN,
    FOLLOWUP_VOLUME_UP_PATTERN,
    SLEEP_PATTERNS,
    MEDIA_PAUSE_PATTERNS,
    NAV_HOME_PATTERNS,
    NAV_BACK_PATTERNS,
    VTV1_PATTERNS,
    VTV2_PATTERNS,
    VTV3_PATTERNS,
)


class SystemIntentClassifier:
    """
    Bộ phân loại phản xạ lệnh hệ thống (Reflex Arc Classifier):
    - Đảm bảo tính tất định, không bao giờ dùng substring matching lỏng lẻo.
    - Có chốt chặn Content Guard: Tuyệt đối không cướp câu lệnh tìm kiếm nội dung (ví dụ: 'mở nhạc hot tiktok').
    - Hiểu các câu nói nối tiếp theo ngữ cảnh (ví dụ: 'bé nữa' sau khi vừa giảm âm lượng).
    """

    @staticmethod
    def classify(
        user_text: str,
        context_state: Optional[ConversationState] = None
    ) -> Optional[ResolvedCommand]:
        text = user_text.strip()
        if not text:
            return None

        # 1. CHỐT CHẶN PHỦ ĐỊNH (Negation Guard)
        # Ví dụ: "Đừng tăng âm lượng nữa", "Không được tắt TV"
        if NEGATION_PREFIX.search(text):
            return None

        # 2. CHỐT CHẶN Ý ĐỊNH NỘI DUNG (Content Intent Guard)
        # Nếu câu bắt đầu bằng "mở nhạc...", "xem phim...", "tìm trên youtube...",
        # câu này chắc chắn thuộc về mảng nội dung, không được nuốt thành lệnh hệ thống!
        if CONTENT_INTENT_PREFIX.search(text) or CONTENT_INTENT_KEYWORD.search(text):
            return None

        # 3. XỬ LÝ CÂU NÓI NỐI TIẾP THEO NGỮ CẢNH (Contextual Follow-ups)
        if context_state:
            # Nếu lượt trước vừa giảm âm lượng và lượt này nói "bé nữa", "nhỏ nữa"
            if FOLLOWUP_VOLUME_DOWN_PATTERN.match(text):
                if context_state.last_action == "volume_down":
                    return ResolvedCommand(
                        action_type=TVActionType.SYSTEM_CONTROL,
                        target="volume_down",
                        feedback="Dạ, cháu đã giảm thêm âm lượng rồi ạ.",
                        confidence=1.0,
                        raw_text=user_text
                    )

            # Nếu lượt trước vừa tăng âm lượng và lượt này nói "to nữa", "tăng nữa"
            if FOLLOWUP_VOLUME_UP_PATTERN.match(text):
                if context_state.last_action == "volume_up":
                    return ResolvedCommand(
                        action_type=TVActionType.SYSTEM_CONTROL,
                        target="volume_up",
                        feedback="Dạ, cháu đã tăng thêm âm lượng rồi ạ.",
                        confidence=1.0,
                        raw_text=user_text
                    )

        # 4. TĂNG ÂM LƯỢNG
        if any(p.search(text) for p in VOLUME_UP_PATTERNS):
            return ResolvedCommand(
                action_type=TVActionType.SYSTEM_CONTROL,
                target="volume_up",
                feedback="Dạ, cháu đã tăng âm lượng rồi ạ.",
                confidence=1.0,
                raw_text=user_text
            )

        # 5. GIẢM ÂM LƯỢNG
        if any(p.search(text) for p in VOLUME_DOWN_PATTERNS):
            return ResolvedCommand(
                action_type=TVActionType.SYSTEM_CONTROL,
                target="volume_down",
                feedback="Dạ, cháu đã giảm âm lượng rồi ạ.",
                confidence=1.0,
                raw_text=user_text
            )

        # 6. TẮT TV / ĐI NGỦ
        if any(p.search(text) for p in SLEEP_PATTERNS):
            return ResolvedCommand(
                action_type=TVActionType.SYSTEM_CONTROL,
                target="sleep",
                feedback="Dạ, chúc ông bà ngủ ngon, cháu tắt TV đây ạ.",
                confidence=1.0,
                raw_text=user_text
            )

        # 7. TẠM DỪNG / TIẾP TỤC
        if any(p.search(text) for p in MEDIA_PAUSE_PATTERNS):
            return ResolvedCommand(
                action_type=TVActionType.SYSTEM_CONTROL,
                target="pause",
                feedback="Dạ, đã gửi lệnh Tạm dừng / Tiếp tục phát.",
                confidence=1.0,
                raw_text=user_text
            )

        # 8. VỀ TRANG CHỦ
        if any(p.search(text) for p in NAV_HOME_PATTERNS):
            return ResolvedCommand(
                action_type=TVActionType.SYSTEM_CONTROL,
                target="home",
                feedback="Dạ, đã quay về màn hình chính.",
                confidence=1.0,
                raw_text=user_text
            )

        # 9. QUAY LẠI TRƯỚC
        if any(p.search(text) for p in NAV_BACK_PATTERNS):
            return ResolvedCommand(
                action_type=TVActionType.SYSTEM_CONTROL,
                target="back",
                feedback="Dạ, đã quay lại màn hình trước.",
                confidence=1.0,
                raw_text=user_text
            )

        # 10. KÊNH THỜI SỰ VTV TRỰC TIẾP
        if any(p.search(text) for p in VTV1_PATTERNS):
            return ResolvedCommand(
                action_type=TVActionType.PLAY_LIVE_TV,
                target="vtv1",
                feedback="Dạ, cháu đang bật kênh thời sự VTV1 cho ông bà ạ.",
                confidence=1.0,
                raw_text=user_text
            )

        if any(p.search(text) for p in VTV2_PATTERNS):
            return ResolvedCommand(
                action_type=TVActionType.PLAY_LIVE_TV,
                target="vtv2",
                feedback="Dạ, cháu đang bật kênh VTV2 cho ông bà ạ.",
                confidence=1.0,
                raw_text=user_text
            )

        if any(p.search(text) for p in VTV3_PATTERNS):
            return ResolvedCommand(
                action_type=TVActionType.PLAY_LIVE_TV,
                target="vtv3",
                feedback="Dạ, cháu đang bật kênh VTV3 cho ông bà ạ.",
                confidence=1.0,
                raw_text=user_text
            )

        return None

