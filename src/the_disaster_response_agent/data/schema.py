from dataclasses import dataclass, field
from typing import Optional

@dataclass
class DisasterEvent:
    text: str
    source: str
    disaster_type: Optional[str] = None
    humanitarian_category: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[str] = None
    timestamp: Optional[str] = None
    raw_metadata: dict = field(default_factory=dict)