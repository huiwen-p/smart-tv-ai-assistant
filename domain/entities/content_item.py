from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any


class LaunchStrategy(str, Enum):
    DIRECT_DEEPLINK = "DIRECT_DEEPLINK"
    MULTI_STEP_WORKFLOW = "MULTI_STEP_WORKFLOW"
    SYSTEM_KEY = "SYSTEM_KEY"


class AvailabilityStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    DEPRECATED = "DEPRECATED"
    UNVERIFIED = "UNVERIFIED"


@dataclass
class ContentItem:
    id: str
    name: str
    category: str  # BUDDHIST, NEWS, TRADITIONAL_MUSIC, COMEDY, SYSTEM
    provider: str  # YOUTUBE, VTVGO, SYSTEM
    launch_strategy: LaunchStrategy = LaunchStrategy.DIRECT_DEEPLINK
    deep_link: Optional[str] = None
    workflow_steps: List[Dict[str, Any]] = field(default_factory=list)
    speaker_or_artist: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    availability: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    default_priority: int = 50
    last_verified: Optional[str] = None

