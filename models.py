"""Data model for a Task."""
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a single task with an ID, title, and completion state."""
    id: int
    title: str
    completed: bool = False
    created_at: Optional[str] = None

    def __post_init__(self):
        """Set created_at if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task instance from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            completed=data.get("completed", False),
            created_at=data.get("created_at", ""),
        )

    def __repr__(self) -> str:
        status = "✓" if self.completed else "✗"
        return f"[{self.id}] {self.title} ({status})"
