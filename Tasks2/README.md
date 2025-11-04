# Task Manager

A simple command-line task management system with knowledge base functionality.

## Features

- Create and manage tasks with priorities and due dates
- List, complete, and delete tasks
- Search through tasks
- Store notes in a knowledge base
- Simple chat assistant interface
- All data stored in JSON files

## Requirements

- Python 3.6 or higher
- No external dependencies needed

## Installation

1. Clone or download this repository
2. Navigate to the `tasks1` directory

```bash
cd tasks1
```

## Running the Application

```bash
python3 task_manager.py
```

Or on Windows:
```bash
python task_manager.py
```

## Usage

### Main Menu Options

When you run the application, you'll see a menu with these options:

1. **List All Tasks** - View all tasks (active and completed)
2. **List Active Tasks** - View only active tasks
3. **List Completed Tasks** - View only completed tasks
4. **Create New Task** - Add a new task
5. **Complete Task** - Mark a task as done
6. **Delete Task** - Permanently remove a task
7. **Search Tasks** - Find tasks by keyword
8. **Add Knowledge Note** - Save a note to your knowledge base
9. **View Knowledge Base** - See all your notes
10. **Delete Knowledge Note** - Permanently remove a note
11. **Chat with Assistant** - Simple command interface
12. **Exit** - Save and quit

### Creating a Task

When creating a task, you'll be prompted for:

- **Title** (required)
- **Description** (optional)
- **Priority**: Low, Medium, High, or Urgent
- **Due Date** (optional, format: YYYY-MM-DD)
- **Tags** (optional, comma-separated)

### Example Usage

**Create a task:**
```
Choose an option: 4

Task Title: Finish homework
Description: Complete CSC299 assignment
Choose priority (1-4): 3
Due date (YYYY-MM-DD): 2025-10-25
Tags: school, programming

✅ Task created: 'Finish homework' (Priority: High)
```

**List active tasks:**
```
Choose an option: 2

=== TASKS ===
Showing: Active Tasks

1. 📌 🟠 Finish homework
   Priority: High | Status: Active
   Due: 2025-10-25
   Description: Complete CSC299 assignment
   Tags: school, programming
```

**Search tasks:**
```
Choose an option: 7

Enter search term: homework

🔍 Found 1 task(s) matching 'homework':

📌 🟠 Finish homework
   Status: Active | Priority: High
   Due: 2025-10-25
```

## Data Storage

All data is automatically saved in the `data/` directory:

```
tasks1/
├── task_manager.py
├── README.md
└── data/
    ├── tasks.json
    └── knowledge.json
```

- **tasks.json** - Stores all your tasks (active and completed)
- **knowledge.json** - Stores your notes

### Backing Up Your Data

To backup your data, simply copy the `data/` folder:

```bash
cp -r data/ data_backup/
```

## Priority Levels

- 🟢 **Low** - Nice to have, no rush
- 🟡 **Medium** - Important, normal timeline
- 🟠 **High** - Very important, do soon
- 🔴 **Urgent** - Critical, do immediately

## Chat Assistant Commands

In the chat interface (option 10), you can use:

- `tasks` - Show all tasks
- `active` - Show active tasks only
- `completed` - Show completed tasks only
- `notes` - Show knowledge base
- `help` - Show available commands
- `exit` - Return to main menu

## Tips

- Use **tags** to organize related tasks (e.g., "work", "personal", "urgent")
- Set **due dates** for time-sensitive tasks
- Use the **knowledge base** to store important information, code snippets, or notes
- **Delete notes** you no longer need to keep your knowledge base organized
- **Search** works on titles, descriptions, priorities, and tags
- Tasks and notes are automatically saved after every action
- Use confirmation prompts carefully - deletions cannot be undone!

## Troubleshooting

**Problem: Application won't start**
- Make sure Python 3.6+ is installed: `python3 --version`
- Check you're in the correct directory: `ls -l task_manager.py`

**Problem: Data not saving**
- Ensure you exit using option 11 (not Ctrl+C)
- Check the `data/` folder has write permissions

**Problem: Can't find tasks**
- Use option 1 to list ALL tasks
- Try searching with option 7

## Future Features

Planned enhancements:
- AI-powered task suggestions
- Recurring tasks
- Task reminders
- Export to CSV/PDF
- Enhanced terminal UI with colors

## Author

Created for CSC299 - Fall 2025

---

**Questions or issues?** Check that all files are saved and you're running the latest version.