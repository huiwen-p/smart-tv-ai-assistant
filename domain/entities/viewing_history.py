from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EventSource(str, Enum):
    VOICE_ASSISTANT = "VOICE_ASSISTANT"
    TV_OBSERVED = "TV_OBSERVED"


class CompletionStatus(str, Enum):
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    SKIPPED = "SKIPPED"
    UNKNOWN = "UNKNOWN"


@dataclass
class ViewingHistoryRecord:
    id: Optional[int] = None
    user_id: str = "grandmother"
    content_id: Optional[str] = None
    title: str = ""
    category: str = ""
    event_type: str = "PLAYED"
    source: EventSource = EventSource.VOICE_ASSISTANT
    started_at: str = ""
    ended_at: Optional[str] = None
    duration_seconds: int = 0
    completion_status: CompletionStatus = CompletionStatus.UNKNOWN
    was_skipped_immediately: bool = False
    raw_utterance: str = ""

