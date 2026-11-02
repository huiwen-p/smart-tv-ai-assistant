from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class InteractionPreferences:
    speech_rate: str = "SLOW"          # SLOW, NORMAL
    confirmation_level: str = "HIGH"   # HIGH, MEDIUM, LOW
    honorific: str = "cháu"            # cháu, con


@dataclass
class UserProfile:
    user_id: str
    name: str = "Bà"
    favorite_categories: List[str] = field(default_factory=lambda: ["BUDDHIST", "NEWS", "TRADITIONAL_MUSIC"])
    favorite_channels: List[str] = field(default_factory=lambda: ["vtv1"])
    favorite_content_ids: List[str] = field(default_factory=list)
    interaction: InteractionPreferences = field(default_factory=InteractionPreferences)
    category_scores: Dict[str, float] = field(default_factory=lambda: {
        "BUDDHIST": 90.0,
        "NEWS": 85.0,
        "TRADITIONAL_MUSIC": 75.0,
        "COMEDY": 60.0
    })

