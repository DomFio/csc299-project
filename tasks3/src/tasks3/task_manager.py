#!/usr/bin/env python3
"""
Simple Task Manager
A command-line task management system with knowledge base and chat interface.

Features:
- Create, list, complete, and delete tasks
- Search through tasks
- Priority levels and due dates
- Tags/categories for organization
- Knowledge base for storing notes
- Simple chat interface (AI integration planned)
"""

import json
import os
from datetime import datetime
from pathlib import Path
import uuid


class TaskManager:
    """Main application class for Task Manager system."""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.tasks_file = self.data_dir / "tasks.json"
        self.knowledge_file = self.data_dir / "knowledge.json"
        
        self.tasks = self.load_tasks()
        self.knowledge = self.load_knowledge()
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "active": [],
                "completed": []
            }
    
    def load_knowledge(self):
        """Load knowledge base from JSON file."""
        if self.knowledge_file.exists():
            with open(self.knowledge_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "notes": []
            }
    
    def save_all(self):
        """Save all data to JSON files."""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
        
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def create_task(self):
        """Create a new task interactively."""
        print("\n=== CREATE NEW TASK ===")
        
        title = input("Task Title: ").strip()
        if not title:
            print("Task title cannot be empty!")
            return
        
        description = input("Description (optional): ").strip()
        
        # Priority selection
        print("\nPriority Levels:")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        print("4. Urgent")
        
        priority_map = {
            "1": "Low",
            "2": "Medium",
            "3": "High",
            "4": "Urgent"
        }
        
        priority_choice = input("Choose priority (1-4, default: Medium): ").strip()
        priority = priority_map.get(priority_choice, "Medium")
        
        # Due date
        due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
        if due_date:
            # Basic validation
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Skipping due date.")
                due_date = None
        else:
            due_date = None
        
        # Tags
        tags = input("Tags (comma-separated, optional): ").strip()
        if tags:
            tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
        else:
            tags = []
        
        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "tags": tags,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.tasks["active"].append(task)
        self.save_all()
        
        print(f"\n✅ Task created: '{title}' (Priority: {priority})")
    
    def list_tasks(self, filter_status=None, sort_by="created"):
        """Display tasks with optional filtering and sorting."""
        print("\n=== TASKS ===")
        
        # Determine which tasks to show
        if filter_status == "active":
            task_list = self.tasks["active"]
            print("Showing: Active Tasks")
        elif filter_status == "completed":
            task_list = self.tasks["completed"]
            print("Showing: Completed Tasks")
        else:
            task_list = self.tasks["active"] + self.tasks["completed"]
            print("Showing: All Tasks")
        
        if not task_list:
            print("No tasks found.")
            return
        
        # Sort tasks
        if sort_by == "created":
            task_list = sorted(task_list, key=lambda x: x["created_at"], reverse=True)
        elif sort_by == "priority":
            priority_order = {"Urgent": 0, "High": 1, "Medium": 2, "Low": 3}
            task_list = sorted(task_list, key=lambda x: priority_order.get(x["priority"], 4))
        elif sort_by == "due_date":
            # Tasks with due dates first, then by date
            task_list = sorted(task_list, key=lambda x: (x["due_date"] is None, x["due_date"] or ""))
        
        # Display tasks
        for idx, task in enumerate(task_list, 1):
            status_icon = "✅" if task["status"] == "completed" else "📌"
            priority_icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Urgent": "🔴"}.get(task["priority"], "⚪")
            
            print(f"\n{idx}. {status_icon} {priority_icon} {task['title']}")
            print(f"   Priority: {task['priority']} | Status: {task['status'].title()}")
            
            if task['due_date']:
                print(f"   Due: {task['due_date']}")
            
            if task['description']:
                print(f"   Description: {task['description']}")
            
            if task['tags']:
                print(f"   Tags: {', '.join(task['tags'])}")
            
            created_date = task['created_at'][:10]
            print(f"   Created: {created_date}")
        
        print(f"\n📊 Total: {len(task_list)} task(s)")
    
    def complete_task(self):
        """Mark a task as completed."""
        print("\n=== COMPLETE TASK ===")
        
        if not self.tasks["active"]:
            print("No active tasks to complete!")
            return
        
        # Show active tasks
        for idx, task in enumerate(self.tasks["active"], 1):
            priority_icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Urgent": "🔴"}.get(task["priority"], "⚪")
            print(f"{idx}. {priority_icon} {task['title']} (Priority: {task['priority']})")
        
        try:
            choice = int(input("\nEnter task number to complete (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.tasks["active"]):
                task = self.tasks["active"][choice - 1]
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                
                # Move to completed
                self.tasks["active"].pop(choice - 1)
                self.tasks["completed"].append(task)
                
                self.save_all()
                
                print(f"\n✅ Task completed: '{task['title']}'")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")
    
    def delete_task(self):
        """Delete a task permanently."""
        print("\n=== DELETE TASK ===")
        print("1. Delete from Active Tasks")
        print("2. Delete from Completed Tasks")
        
        choice = input("\nChoose option (1-2, 0 to cancel): ").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            task_list = self.tasks["active"]
            list_name = "active"
        elif choice == "2":
            task_list = self.tasks["completed"]
            list_name = "completed"
        else:
            print("Invalid option!")
            return
        
        if not task_list:
            print(f"No {list_name} tasks to delete!")
            return
        
        # Show tasks
        for idx, task in enumerate(task_list, 1):
            print(f"{idx}. {task['title']}")
        
        try:
            task_choice = int(input(f"\nEnter task number to delete (0 to cancel): "))
            if task_choice == 0:
                return
            
            if 1 <= task_choice <= len(task_list):
                task = task_list[task_choice - 1]
                confirm = input(f"Delete '{task['title']}'? This cannot be undone. (yes/no): ").strip().lower()
                
                if confirm == "yes":
                    task_list.pop(task_choice - 1)
                    self.save_all()
                    print(f"\n🗑️  Task deleted: '{task['title']}'")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")
    
    def search_tasks(self):
        """Search through all tasks."""
        print("\n=== SEARCH TASKS ===")
        keyword = input("Enter search term: ").strip().lower()
        
        if not keyword:
            print("Search term cannot be empty!")
            return
        
        results = []
        
        # Search active tasks
        for task in self.tasks["active"]:
            if (keyword in task["title"].lower() or 
                keyword in task["description"].lower() or
                keyword in task["priority"].lower() or
                any(keyword in tag.lower() for tag in task["tags"])):
                results.append((task, "active"))
        
        # Search completed tasks
        for task in self.tasks["completed"]:
            if (keyword in task["title"].lower() or 
                keyword in task["description"].lower() or
                keyword in task["priority"].lower() or
                any(keyword in tag.lower() for tag in task["tags"])):
                results.append((task, "completed"))
        
        if not results:
            print(f"\n❌ No tasks found matching '{keyword}'")
            return
        
        print(f"\n🔍 Found {len(results)} task(s) matching '{keyword}':\n")
        
        for task, status in results:
            status_icon = "✅" if status == "completed" else "📌"
            priority_icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Urgent": "🔴"}.get(task["priority"], "⚪")
            
            print(f"{status_icon} {priority_icon} {task['title']}")
            print(f"   Status: {status.title()} | Priority: {task['priority']}")
            if task['due_date']:
                print(f"   Due: {task['due_date']}")
            if task['description']:
                print(f"   Description: {task['description']}")
            if task['tags']:
                print(f"   Tags: {', '.join(task['tags'])}")
            print()
    
    def add_note(self):
        """Add a note to knowledge base."""
        print("\n=== ADD KNOWLEDGE NOTE ===")
        
        title = input("Note Title: ").strip()
        if not title:
            print("Note title cannot be empty!")
            return
        
        content = input("Note Content: ").strip()
        
        tags = input("Tags (comma-separated, optional): ").strip()
        if tags:
            tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
        else:
            tags = []
        
        note = {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "tags": tags,
            "created_at": datetime.now().isoformat()
        }
        
        self.knowledge["notes"].append(note)
        self.save_all()
        
        print(f"\n📝 Note saved: '{title}'")
    
    def view_notes(self):
        """Display all knowledge notes."""
        print("\n=== KNOWLEDGE BASE ===")
        
        if not self.knowledge["notes"]:
            print("No notes yet. Add some to build your knowledge base!")
            return
        
        for idx, note in enumerate(self.knowledge["notes"], 1):
            print(f"\n{idx}. 📝 {note['title']}")
            print(f"   {note['content']}")
            if note['tags']:
                print(f"   Tags: {', '.join(note['tags'])}")
            created_date = note['created_at'][:10]
            print(f"   Created: {created_date}")
        
        print(f"\n📊 Total: {len(self.knowledge['notes'])} note(s)")
    
    def delete_note(self):
        """Delete a note from knowledge base."""
        print("\n=== DELETE KNOWLEDGE NOTE ===")
        
        if not self.knowledge["notes"]:
            print("No notes to delete!")
            return
        
        # Show all notes
        for idx, note in enumerate(self.knowledge["notes"], 1):
            print(f"{idx}. 📝 {note['title']}")
        
        try:
            choice = int(input("\nEnter note number to delete (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.knowledge["notes"]):
                note = self.knowledge["notes"][choice - 1]
                confirm = input(f"Delete '{note['title']}'? This cannot be undone. (yes/no): ").strip().lower()
                
                if confirm == "yes":
                    self.knowledge["notes"].pop(choice - 1)
                    self.save_all()
                    print(f"\n🗑️  Note deleted: '{note['title']}'")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid note number!")
        except ValueError:
            print("Please enter a valid number!")
    
    def delete_note(self):
        """Delete a note from knowledge base."""
        print("\n=== DELETE KNOWLEDGE NOTE ===")
        
        if not self.knowledge["notes"]:
            print("No notes to delete!")
            return
        
        # Show all notes
        for idx, note in enumerate(self.knowledge["notes"], 1):
            print(f"{idx}. 📝 {note['title']}")
        
        try:
            choice = int(input("\nEnter note number to delete (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.knowledge["notes"]):
                note = self.knowledge["notes"][choice - 1]
                confirm = input(f"Delete '{note['title']}'? This cannot be undone. (yes/no): ").strip().lower()
                
                if confirm == "yes":
                    self.knowledge["notes"].pop(choice - 1)
                    self.save_all()
                    print(f"\n🗑️  Note deleted: '{note['title']}'")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid note number!")
        except ValueError:
            print("Please enter a valid number!")
    
    def simple_chat(self):
        """Simple chat interface (AI integration planned)."""
        print("\n=== TASK ASSISTANT ===")
        print("(Simple version - AI integration coming soon!)")
        print("\nAvailable commands:")
        print("  'tasks' - Show all tasks")
        print("  'active' - Show active tasks")
        print("  'completed' - Show completed tasks")
        print("  'notes' - Show knowledge base")
        print("  'help' - Show available commands")
        print("  'exit' - Return to main menu")
        
        while True:
            user_input = input("\nYou: ").strip().lower()
            
            if user_input == "exit":
                break
            elif user_input == "tasks":
                self.list_tasks()
            elif user_input == "active":
                self.list_tasks(filter_status="active")
            elif user_input == "completed":
                self.list_tasks(filter_status="completed")
            elif user_input == "notes":
                self.view_notes()
            elif user_input == "help":
                print("\nAssistant: Available commands:")
                print("  'tasks', 'active', 'completed', 'notes', 'help', 'exit'")
            else:
                print("\nAssistant: I don't understand that command. Type 'help' for available commands.")
    
    def main_menu(self):
        """Display main menu and handle user input."""
        while True:
            print("\n" + "="*50)
            print("TASK MANAGER".center(50))
            print("="*50)
            
            active_count = len(self.tasks["active"])
            completed_count = len(self.tasks["completed"])
            print(f"\nActive Tasks: {active_count} | Completed: {completed_count}")
            
            print("\n1. 📋 List All Tasks")
            print("2. 📌 List Active Tasks")
            print("3. ✅ List Completed Tasks")
            print("4. ➕ Create New Task")
            print("5. ✔️  Complete Task")
            print("6. 🗑️  Delete Task")
            print("7. 🔍 Search Tasks")
            print("8. 📝 Add Knowledge Note")
            print("9. 📚 View Knowledge Base")
            print("10. 🗑️  Delete Knowledge Note")
            print("11. 💬 Chat with Assistant")
            print("12. 🚪 Exit")
            
            choice = input("\nChoose an option: ").strip()
            
            if choice == "1":
                self.list_tasks()
            elif choice == "2":
                self.list_tasks(filter_status="active")
            elif choice == "3":
                self.list_tasks(filter_status="completed")
            elif choice == "4":
                self.create_task()
            elif choice == "5":
                self.complete_task()
            elif choice == "6":
                self.delete_task()
            elif choice == "7":
                self.search_tasks()
            elif choice == "8":
                self.add_note()
            elif choice == "9":
                self.view_notes()
            elif choice == "10":
                self.delete_note()
            elif choice == "11":
                self.simple_chat()
            elif choice == "12":
                print("\n📁 All changes saved. Goodbye!\n")
                break
            else:
                print("\n❌ Invalid option! Please choose 1-12.")


def main():
    """Entry point for the application."""
    print("\n" + "="*50)
    print("TASK MANAGER".center(50))
    print("="*50)
    print("\nA simple command-line task management system.")
    print("Organize your tasks, track progress, and build your knowledge base.\n")
    
    app = TaskManager()
    app.main_menu()


if __name__ == "__main__":
    main()