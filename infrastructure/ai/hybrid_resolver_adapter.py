from typing import Optional, List, Dict, Any
from domain.entities.intent import TVActionType, ResolvedCommand
from domain.entities.content_item import ContentItem
from domain.entities.conversation_state import ConversationState
from application.ports.ai_resolver_port import BaseAIResolverPort
from application.intent.intent_classifier import SystemIntentClassifier
from infrastructure.ai.gemini_resolver_adapter import GeminiAIResolverAdapter


class HybridAIResolverAdapter(BaseAIResolverPort):
    """
    Bộ phân loại ý định lai ghép (Hybrid Architecture):
    - Fast-Path (0ms Offline): Khớp bằng SystemIntentClassifier cho các thao tác hệ thống
      (âm lượng, tắt TV/đi ngủ, tạm dừng/tiếp tục, điều hướng Home/Back, mở kênh VTV).
    - AI-Path: Ủy quyền toàn bộ cho Gemini LLM (kèm Candidate Retrieval) khi gặp khẩu ngữ tự nhiên.
    """

    def __init__(self, gemini_adapter: Optional[GeminiAIResolverAdapter] = None):
        self.ai = gemini_adapter or GeminiAIResolverAdapter()

    def resolve(
        self,
        user_text: str,
        candidates: Optional[List[ContentItem]] = None,
        context_hints: Optional[Dict[str, Any]] = None
    ) -> ResolvedCommand:
        # Trích xuất state từ context_hints nếu có
        context_state = None
        if context_hints and "state" in context_hints:
            context_state = context_hints["state"]

        # 1. FAST-PATH (Phản xạ tủy sống 0ms Offline cho lệnh hệ thống dứt khoát)
        fast_cmd = SystemIntentClassifier.classify(user_text, context_state=context_state)
        if fast_cmd is not None:
            return fast_cmd

        # 2. AI-PATH (Ủy quyền toàn bộ cho Gemini LLM / Context-Aware Fallback)
        return self.ai.resolve(user_text, candidates, context_hints)
