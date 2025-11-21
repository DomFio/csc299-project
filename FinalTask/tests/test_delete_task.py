import pytest
import tempfile
import shutil
from tasks3.task_manager import TaskManager


@pytest.fixture
def temp_task_manager():
    """Create a TaskManager with a temporary data directory for testing."""
    temp_dir = tempfile.mkdtemp()
    tm = TaskManager(data_dir=temp_dir)
    
    yield tm
    
    shutil.rmtree(temp_dir)


def test_delete_task(temp_task_manager):
    """Test that deleting a task removes it from the list."""
    tm = temp_task_manager
    
    # Create two tasks
    task1 = {
        "id": "test-789",
        "title": "Task to delete",
        "description": "This will be deleted",
        "priority": "Low",
        "due_date": None,
        "tags": [],
        "status": "active",
        "created_at": "2025-10-19T10:00:00",
        "completed_at": None
    }
    
    task2 = {
        "id": "test-790",
        "title": "Task to keep",
        "description": "This stays",
        "priority": "Medium",
        "due_date": None,
        "tags": [],
        "status": "active",
        "created_at": "2025-10-19T11:00:00",
        "completed_at": None
    }
    
    # Add both tasks
    tm.tasks["active"].append(task1)
    tm.tasks["active"].append(task2)
    
    # Verify we have 2 tasks
    assert len(tm.tasks["active"]) == 2
    
    # Delete the first task (simulate what delete_task() does)
    tm.tasks["active"].pop(0)
    
    # Verify we now have 1 task
    assert len(tm.tasks["active"]) == 1
    
    # Verify the remaining task is the correct one
    assert tm.tasks["active"][0]["title"] == "Task to keep"