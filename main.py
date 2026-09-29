"""Command-line interface for TaskFlow CLI."""
import argparse
import sys

from .models import Task
from .storage import TaskStorage
from .task_manager import TaskManager


def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for CLI commands."""
    parser = argparse.ArgumentParser(
        prog="taskflow",
        description="A simple command-line Todo management application.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task")

    # List command
    subparsers.add_parser("list", help="List all tasks")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark a task as completed")
    done_parser.add_argument("id", type=int, help="ID of the task to complete")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="ID of the task to delete")

    return parser


def format_task(task: Task) -> str:
    """Format a task for display."""
    status = "✓" if task.completed else "✗"
    return f"[{task.id}] {task.title} ({status})"


def main():
    """Main entry point for the TaskFlow CLI."""
    parser = create_parser()
    args = parser.parse_args()

    storage = TaskStorage("tasks.json")
    manager = TaskManager(storage)

    if args.command == "add":
        try:
            task = manager.add(args.title)
            print(f"Added: {format_task(task)}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "list":
        tasks = manager.list()
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(format_task(task))

    elif args.command == "done":
        try:
            task = manager.complete(args.id)
            print(f"Completed: {format_task(task)}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "delete":
        try:
            manager.delete(args.id)
            print(f"Deleted task {args.id}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()