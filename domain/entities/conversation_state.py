import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any


class DialogueState(str, Enum):
    IDLE = "IDLE"
    AWAITING_CLARIFICATION = "AWAITING_CLARIFICATION"
    EXECUTING = "EXECUTING"


@dataclass
class ConversationState:
    session_id: str = "default_session"
    active_intent: Optional[str] = None
    pending_slot: Optional[str] = None
    slots: Dict[str, Any] = field(default_factory=dict)
    last_candidate_ids: List[str] = field(default_factory=list)
    currently_playing_id: Optional[str] = None
    last_action: Optional[str] = None
    dialogue_state: DialogueState = DialogueState.IDLE
    last_updated: float = field(default_factory=time.time)
    ttl_seconds: float = 90.0

    def is_expired(self) -> bool:
        return (time.time() - self.last_updated) > self.ttl_seconds

    def touch(self):
        self.last_updated = time.time()

    def reset(self):
        self.active_intent = None
        self.pending_slot = None
        self.slots = {}
        self.last_candidate_ids = []
        self.dialogue_state = DialogueState.IDLE
        self.touch()

