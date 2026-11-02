from typing import List, Optional
from domain.entities.intent import TVActionType, ResolvedCommand, IntentConfidence
from domain.entities.content_item import ContentItem
from domain.entities.conversation_state import ConversationState, DialogueState
from application.ports.ai_resolver_port import BaseAIResolverPort


class ResolveUserIntentUseCase:
    """
    Use Case phân loại ý định 3 trạng thái:
    - Đủ thông tin (>= 0.85 hoặc System Control): Thực thi ngay.
    - Có nhiều khả năng nội dung (0.60 - 0.84): Hỏi lại lễ phép (Clarification).
    - Không hiểu (< 0.60): Yêu cầu diễn đạt lại hoặc tìm kiếm.
    """

    def __init__(self, ai_resolver: BaseAIResolverPort):
        self.ai = ai_resolver

    def execute(
        self,
        raw_text: str,
        candidates: List[ContentItem],
        state: ConversationState
    ) -> ResolvedCommand:
        # Nếu đang trong trạng thái chờ giải đáp làm rõ (Awaiting Clarification)
        if state.dialogue_state == DialogueState.AWAITING_CLARIFICATION and state.last_candidate_ids:
            return self._handle_clarification_reply(raw_text, state, candidates)

        # Gửi sang AI Resolver cùng danh sách ứng viên hợp lệ
        resolved = self.ai.resolve(
            raw_text,
            candidates=candidates,
            context_hints={"active_intent": state.active_intent, "state": state}
        )

        # -------------------------------------------------------------
        # ĐÁNH GIÁ Ý ĐỊNH & PHÂN NHÁNH AN TOÀN
        # -------------------------------------------------------------
        # 1. Các lệnh điều khiển hệ thống (âm lượng, tắt TV, pause, home, back)
        # hoặc kênh thời sự trực tiếp (VTV1/2/3): LUÔN THỰC THI NGAY
        if resolved.action_type in [TVActionType.SYSTEM_CONTROL, TVActionType.PLAY_LIVE_TV]:
            state.dialogue_state = DialogueState.EXECUTING
            state.active_intent = resolved.action_type.value
            state.touch()
            return resolved

        # 2. Lệnh tìm kiếm YouTube tự do: Thực thi ngay
        if resolved.action_type == TVActionType.SEARCH_YOUTUBE:
            state.dialogue_state = DialogueState.EXECUTING
            state.active_intent = resolved.action_type.value
            state.touch()
            return resolved

        # 3. Lệnh mở nội dung cụ thể có ID rõ ràng hoặc độ tin cậy cao
        if resolved.action_type == TVActionType.PLAY_CONTENT and (resolved.content_id or resolved.confidence >= 0.85):
            state.dialogue_state = DialogueState.EXECUTING
            state.active_intent = resolved.action_type.value
            state.touch()
            return resolved

        # 4. Khi ý định là CLARIFY hoặc cần làm rõ giữa các ứng viên nội dung (chỉ khi có candidates liên quan)
        if resolved.action_type == TVActionType.CLARIFY or (0.60 <= resolved.confidence < 0.85 and len(candidates) >= 2):
            c1, c2 = candidates[0], candidates[1]
            feedback = resolved.feedback if resolved.action_type == TVActionType.CLARIFY and resolved.feedback else f"Dạ, bà muốn nghe {c1.name} hay {c2.name} ạ?"
            state.dialogue_state = DialogueState.AWAITING_CLARIFICATION
            state.last_candidate_ids = [c1.id, c2.id]
            state.touch()

            return ResolvedCommand(
                action_type=TVActionType.CLARIFY,
                feedback=feedback,
                confidence=resolved.confidence,
                raw_text=raw_text,
                clarification_options=[c1.name, c2.name]
            )

        # 5. Còn lại: Quá mơ hồ -> Yêu cầu nói lại
        state.reset()
        return ResolvedCommand(
            action_type=TVActionType.CLARIFY,
            feedback="Dạ, cháu chưa nghe rõ ý bà, bà muốn xem thời sự hay nghe kinh Phật ạ?",
            confidence=0.4,
            raw_text=raw_text
        )

    def _handle_clarification_reply(
        self,
        raw_text: str,
        state: ConversationState,
        candidates: List[ContentItem]
    ) -> ResolvedCommand:
        """Xử lý câu trả lời ngắn gọn khi ông bà chọn một trong các phương án."""
        text_lower = raw_text.lower().strip()
        matched_item = None

        # Kiểm tra câu nói có nhắc tới tên ứng viên nào không
        for c_id in state.last_candidate_ids:
            item = next((c for c in candidates if c.id == c_id), None)
            if item and (item.name.lower() in text_lower or any(t in text_lower for t in item.tags)):
                matched_item = item
                break

        # Nếu nói "cái thứ nhất", "bài đầu tiên", "bài một"
        if not matched_item:
            if any(w in text_lower for w in ["thứ nhất", "đầu tiên", "bài 1", "cái một", "cái trước", "bài đầu"]):
                matched_item = next((c for c in candidates if c.id == state.last_candidate_ids[0]), None)
            elif any(w in text_lower for w in ["thứ hai", "bài 2", "cái hai", "cái sau"]):
                if len(state.last_candidate_ids) > 1:
                    matched_item = next((c for c in candidates if c.id == state.last_candidate_ids[1]), None)

        if matched_item:
            state.dialogue_state = DialogueState.EXECUTING
            state.touch()
            return ResolvedCommand(
                action_type=TVActionType.PLAY_CONTENT,
                target=matched_item.deep_link or "",
                content_id=matched_item.id,
                feedback=f"Dạ, cháu mở {matched_item.name} cho bà ngay đây ạ.",
                confidence=0.95,
                raw_text=raw_text
            )

        # Nếu không khớp với các lựa chọn làm rõ, người dùng có thể đã đổi ý hoặc ra lệnh mới
        state.reset()
        return self.execute(raw_text, candidates, state)
