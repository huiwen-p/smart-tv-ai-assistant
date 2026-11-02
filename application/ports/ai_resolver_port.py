from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.intent import ResolvedCommand
from domain.entities.content_item import ContentItem


class BaseAIResolverPort(ABC):
    """Cổng giao tiếp trừu tượng phân tích ý định ngôn ngữ tự nhiên."""

    @abstractmethod
    def resolve(
        self,
        user_text: str,
        candidates: Optional[List[ContentItem]] = None,
        context_hints: Optional[dict] = None
    ) -> ResolvedCommand:
        """Phân tích câu nói thành ResolvedCommand có cấu trúc."""
        pass

