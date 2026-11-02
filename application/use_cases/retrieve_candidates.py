import re
from typing import List, Optional, Tuple
from domain.entities.content_item import ContentItem
from application.ports.repository_ports import (
    ContentRepositoryPort,
    HistoryRepositoryPort,
    PreferenceRepositoryPort
)


class RetrieveCandidatesUseCase:
    """
    Candidate Retrieval Module:
    Truy xuất và xếp hạng 3-5 nội dung tiềm năng nhất từ Catalog & Lịch sử
    trước khi đưa cho LLM lựa chọn. Tuyệt đối không gửi toàn bộ dữ liệu mù cho AI.
    """

    def __init__(
        self,
        content_repo: ContentRepositoryPort,
        history_repo: HistoryRepositoryPort,
        preference_repo: PreferenceRepositoryPort
    ):
        self.content_repo = content_repo
        self.history_repo = history_repo
        self.preference_repo = preference_repo

    def execute(
        self,
        query_text: str,
        temporal_reference: Optional[str] = None,
        category_hint: Optional[str] = None,
        limit: int = 5
    ) -> List[ContentItem]:
        candidates: List[ContentItem] = []
        user_scores = self.preference_repo.get_preference_scores()

        # 1. Nếu có tham chiếu thời gian (hôm qua, vừa rồi, sáng nay) -> Ưu tiên Lịch sử xem
        if temporal_reference:
            ref_lower = temporal_reference.lower()
            if "hôm qua" in ref_lower or "yesterday" in ref_lower:
                recent = self.history_repo.get_recent_history(limit=10)
                for rec in recent:
                    if rec.content_id:
                        item = self.content_repo.get_by_id(rec.content_id)
                        if item and item not in candidates:
                            candidates.append(item)
            elif "vừa rồi" in ref_lower or "trước đó" in ref_lower or "vừa nghe" in ref_lower:
                last_played = self.history_repo.get_last_played()
                if last_played and last_played.content_id:
                    item = self.content_repo.get_by_id(last_played.content_id)
                    if item:
                        candidates.append(item)

        # 2. Lọc theo thể loại nếu được gợi ý (ví dụ: BUDDHIST, NEWS)
        if category_hint:
            cat_items = self.content_repo.search_by_category(category_hint, limit=limit)
            for it in cat_items:
                if it not in candidates:
                    candidates.append(it)

        # 3. Tìm kiếm theo từ khóa văn bản (Keyword / Tag Search)
        kw_items = self.content_repo.search_by_keyword(query_text, limit=limit)
        for it in kw_items:
            if it not in candidates:
                candidates.append(it)

        # 4. Nếu chưa đủ ứng viên, nạp thêm các nội dung có điểm ưu tiên cao nhất của người dùng
        if len(candidates) < limit:
            all_items = self.content_repo.list_all()
            # Xếp theo điểm sở thích
            sorted_items = sorted(
                all_items,
                key=lambda x: user_scores.get(x.id, x.default_priority),
                reverse=True
            )
            for it in sorted_items:
                if it not in candidates:
                    candidates.append(it)
                if len(candidates) >= limit:
                    break

        return candidates[:limit]

