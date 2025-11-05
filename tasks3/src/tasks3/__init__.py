def inc(n: int) -> int:
    return n + 1

from tasks3.task_manager import TaskManager

def main():
    """Entry point for the task manager application."""
    app = TaskManager()
    app.main_menu()
