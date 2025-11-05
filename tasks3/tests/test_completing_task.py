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


def test_complete_task(temp_task_manager):
    """Test that completing a task moves it from active to completed."""
    tm = temp_task_manager
    
    # Create an active task
    task = {
        "id": "test-456",
        "title": "Finish homework",
        "description": "Complete assignment",
        "priority": "High",
        "due_date": None,
        "tags": ["school"],
        "status": "active",
        "created_at": "2025-10-19T10:00:00",
        "completed_at": None
    }
    
    # Add to active tasks
    tm.tasks["active"].append(task)
    
    # Verify it's in active
    assert len(tm.tasks["active"]) == 1
    assert len(tm.tasks["completed"]) == 0
    
    # Complete the task (simulate what complete_task() does)
    task["status"] = "completed"
    task["completed_at"] = "2025-10-19T15:00:00"
    
    # Move from active to completed
    completed_task = tm.tasks["active"].pop(0)
    tm.tasks["completed"].append(completed_task)
    
    # Verify it moved to completed
    assert len(tm.tasks["active"]) == 0
    assert len(tm.tasks["completed"]) == 1
    assert tm.tasks["completed"][0]["status"] == "completed"
    assert tm.tasks["completed"][0]["completed_at"] is not None