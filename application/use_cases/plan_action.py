from domain.entities.intent import TVActionType, ResolvedCommand
from domain.entities.content_item import ContentItem, LaunchStrategy


class PlanActionUseCase:
    """
    Action Planner & Policy Gate:
    Chuyển ResolvedCommand thành kế hoạch hành động cụ thể cho thiết bị.
    Kiểm tra an toàn đối với các lệnh nhạy cảm (tắt TV, thoát ứng dụng).
    """

    def execute(self, cmd: ResolvedCommand, content_item: ContentItem = None) -> ResolvedCommand:
        # 1. Kiểm tra chính sách an toàn (Policy Gate)
        if cmd.action_type == TVActionType.SYSTEM_CONTROL and cmd.target == "sleep":
            if cmd.confidence < 0.80:
                # Nếu không chắc chắn người dùng muốn tắt TV, chuyển thành hỏi lại
                cmd.action_type = TVActionType.CLARIFY
                cmd.feedback = "Dạ, có phải ông bà muốn tắt TV để đi ngủ không ạ?"
                return cmd

        # 2. Xử lý mở nội dung theo chiến lược (Direct DeepLink vs Workflow)
        if content_item:
            if content_item.launch_strategy == LaunchStrategy.DIRECT_DEEPLINK:
                cmd.target = content_item.deep_link or ""
            elif content_item.launch_strategy == LaunchStrategy.SYSTEM_KEY:
                cmd.action_type = TVActionType.SYSTEM_CONTROL
                cmd.target = content_item.deep_link or "home"

        return cmd

