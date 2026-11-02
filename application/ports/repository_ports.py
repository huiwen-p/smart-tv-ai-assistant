from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from domain.entities.content_item import ContentItem
from domain.entities.viewing_history import ViewingHistoryRecord
from domain.entities.user_profile import UserProfile


class ContentRepositoryPort(ABC):
    @abstractmethod
    def get_by_id(self, content_id: str) -> Optional[ContentItem]:
        pass

    @abstractmethod
    def search_by_category(self, category: str, limit: int = 5) -> List[ContentItem]:
        pass

    @abstractmethod
    def search_by_keyword(self, keyword: str, limit: int = 5) -> List[ContentItem]:
        pass

    @abstractmethod
    def list_all(self) -> List[ContentItem]:
        pass

    @abstractmethod
    def save(self, item: ContentItem) -> bool:
        pass


class HistoryRepositoryPort(ABC):
    @abstractmethod
    def record_event(self, record: ViewingHistoryRecord) -> int:
        pass

    @abstractmethod
    def get_recent_history(self, user_id: str = "grandmother", limit: int = 10) -> List[ViewingHistoryRecord]:
        pass

    @abstractmethod
    def get_history_by_temporal_range(self, start_date_str: str, end_date_str: str) -> List[ViewingHistoryRecord]:
        pass

    @abstractmethod
    def get_last_played(self, user_id: str = "grandmother") -> Optional[ViewingHistoryRecord]:
        pass


class PreferenceRepositoryPort(ABC):
    @abstractmethod
    def get_user_profile(self, user_id: str = "grandmother") -> UserProfile:
        pass

    @abstractmethod
    def update_preference_score(self, user_id: str, item_key: str, item_type: str, delta: float) -> float:
        pass

    @abstractmethod
    def get_preference_scores(self, user_id: str = "grandmother") -> Dict[str, float]:
        pass

