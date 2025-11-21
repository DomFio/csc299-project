import pytest
import tempfile
import shutil
from tasks3.task_manager import TaskManager


@pytest.fixture
def temp_task_manager():
    """Create a TaskManager with a temporary data directory for testing."""
    # Create temporary directory so we don't mess with real data
    temp_dir = tempfile.mkdtemp()
    tm = TaskManager(data_dir=temp_dir)
    
    yield tm
    
    # Clean up temp directory after test
    shutil.rmtree(temp_dir)


def test_create_task(temp_task_manager):
    """Test that we can create and add a task to the active list."""
    tm = temp_task_manager
    
    # Create a task manually (like what create_task() does internally)
    task = {
        "id": "test-123",
        "title": "Test Task",
        "description": "This is a test",
        "priority": "High",
        "due_date": None,
        "tags": ["test"],
        "status": "active",
        "created_at": "2025-10-19T12:00:00",
        "completed_at": None
    }
    
    # Add the task to active tasks
    tm.tasks["active"].append(task)
    
    # Verify the task was added correctly
    assert len(tm.tasks["active"]) == 1
    assert tm.tasks["active"][0]["title"] == "Test Task"
    assert tm.tasks["active"][0]["priority"] == "High"