"""Storage layer for persisting tasks to a JSON file."""
import json
import os
from typing import List

from .models import Task


class TaskStorage:
    """Handles reading and writing tasks to a JSON file."""

    def __init__(self, filepath: str = "tasks.json"):
        """Initialize storage with the given filepath."""
        self.filepath = filepath

    def load(self) -> List[Task]:
        """Load all tasks from the JSON file. Returns empty list if file doesn't exist."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            return []

    def save(self, tasks: List[Task]) -> None:
        """Save all tasks to the JSON file."""
        parent_dir = os.path.dirname(self.filepath)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)
