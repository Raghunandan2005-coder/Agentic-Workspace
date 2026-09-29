"""Core task manager business logic."""
from typing import List, Optional

from .models import Task
from .storage import TaskStorage


class TaskManager:
    """Manages the collection of tasks with add, list, complete, and delete operations."""

    def __init__(self, storage: TaskStorage):
        """Initialize the task manager with a storage backend."""
        self.storage = storage
        self._tasks: List[Task] = []
        self._next_id: int = 1
        self._load()

    def _load(self) -> None:
        """Load tasks from storage and set the next available ID."""
        self._tasks = self.storage.load()
        if self._tasks:
            self._next_id = max(task.id for task in self._tasks) + 1
        else:
            self._next_id = 1

    def _save(self) -> None:
        """Persist current tasks to storage."""
        self.storage.save(self._tasks)

    def add(self, title: str) -> Task:
        """Add a new task with the given title. Raises ValueError if title is empty."""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")
        task = Task(id=self._next_id, title=title.strip())
        self._tasks.append(task)
        self._next_id += 1
        self._save()
        return task

    def list(self) -> List[Task]:
        """Return a list of all tasks."""
        return list(self._tasks)

    def complete(self, task_id: int) -> Task:
        """Mark the task with the given ID as completed. Raises ValueError if not found."""
        for task in self._tasks:
            if task.id == task_id:
                task.completed = True
                self._save()
                return task
        raise ValueError(f"Task with ID {task_id} not found.")

    def delete(self, task_id: int) -> None:
        """Delete the task with the given ID. Raises ValueError if not found."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                self._save()
                return
        raise ValueError(f"Task with ID {task_id} not found.")

    def get(self, task_id: int) -> Optional[Task]:
        """Retrieve a specific task by ID. Returns None if not found."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def clear_completed(self) -> int:
        """Remove all completed tasks. Returns the number of tasks removed."""
        count = sum(1 for task in self._tasks if task.completed)
        self._tasks = [task for task in self._tasks if not task.completed]
        self._save()
        return count
