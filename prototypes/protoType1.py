#!/usr/bin/env python3
"""
Quest Log - Prototype v1
A gamified task management system with RPG mechanics.

This prototype demonstrates:
- Basic quest management (create, complete, view)
- XP and leveling system
- JSON persistence
- Simple terminal interface
- Basic achievement tracking
"""

import json
import os
from datetime import datetime
from pathlib import Path
import uuid


class QuestLog:
    """Main application class for Quest Log system."""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.player_file = self.data_dir / "player.json"
        self.quests_file = self.data_dir / "quests.json"
        self.knowledge_file = self.data_dir / "knowledge.json"
        
        self.player = self.load_player()
        self.quests = self.load_quests()
        self.knowledge = self.load_knowledge()
    
    def load_player(self):
        """Load player data or create new player."""
        if self.player_file.exists():
            with open(self.player_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "name": "Adventurer",
                "level": 1,
                "xp": 0,
                "total_xp": 0,
                "quests_completed": 0,
                "achievements": [],
                "skills": {
                    "productivity": 0,
                    "learning": 0,
                    "health": 0,
                    "creativity": 0
                }
            }
    
    def load_quests(self):
        """Load quests from JSON file."""
        if self.quests_file.exists():
            with open(self.quests_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "active": [],
                "completed": [],
                "templates": []
            }
    
    def load_knowledge(self):
        """Load knowledge base from JSON file."""
        if self.knowledge_file.exists():
            with open(self.knowledge_file, 'r') as f:
                return json.load(f)
        else:
            return {
                "notes": [],
                "playbooks": [],
                "motivations": []
            }
    
    def save_all(self):
        """Save all data to JSON files."""
        with open(self.player_file, 'w') as f:
            json.dump(self.player, f, indent=2)
        
        with open(self.quests_file, 'w') as f:
            json.dump(self.quests, f, indent=2)
        
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def calculate_xp_for_level(self, level):
        """Calculate XP needed for a given level (exponential curve)."""
        return int(100 * (1.5 ** (level - 1)))
    
    def add_xp(self, amount):
        """Add XP to player and handle leveling up."""
        self.player["xp"] += amount
        self.player["total_xp"] += amount
        
        # Check for level up
        xp_needed = self.calculate_xp_for_level(self.player["level"])
        while self.player["xp"] >= xp_needed:
            self.player["xp"] -= xp_needed
            self.player["level"] += 1
            print(f"\n🎉 LEVEL UP! You are now level {self.player['level']}! 🎉")
            xp_needed = self.calculate_xp_for_level(self.player["level"])
    
    def create_quest(self):
        """Create a new quest interactively."""
        print("\n=== CREATE NEW QUEST ===")
        title = input("Quest Title: ").strip()
        if not title:
            print("Quest title cannot be empty!")
            return
        
        description = input("Description: ").strip()
        
        print("\nDifficulty Levels:")
        print("1. Trivial (10 XP)")
        print("2. Easy (25 XP)")
        print("3. Medium (50 XP)")
        print("4. Hard (100 XP)")
        print("5. Epic (250 XP)")
        
        difficulty_map = {
            "1": ("Trivial", 10),
            "2": ("Easy", 25),
            "3": ("Medium", 50),
            "4": ("Hard", 100),
            "5": ("Epic", 250)
        }
        
        difficulty_choice = input("Choose difficulty (1-5): ").strip()
        difficulty, xp_reward = difficulty_map.get(difficulty_choice, ("Medium", 50))
        
        print("\nQuest Type:")
        print("1. Main Quest (big goals)")
        print("2. Side Quest (optional tasks)")
        print("3. Daily Quest (routine habits)")
        
        quest_type_map = {
            "1": "main",
            "2": "side",
            "3": "daily"
        }
        
        type_choice = input("Choose type (1-3): ").strip()
        quest_type = quest_type_map.get(type_choice, "side")
        
        # Skill association
        print("\nPrimary Skill:")
        print("1. Productivity")
        print("2. Learning")
        print("3. Health")
        print("4. Creativity")
        
        skill_map = {
            "1": "productivity",
            "2": "learning",
            "3": "health",
            "4": "creativity"
        }
        
        skill_choice = input("Choose skill (1-4): ").strip()
        skill = skill_map.get(skill_choice, "productivity")
        
        quest = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "difficulty": difficulty,
            "xp_reward": xp_reward,
            "type": quest_type,
            "skill": skill,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.quests["active"].append(quest)
        self.save_all()
        
        print(f"\n✨ Quest created: '{title}' ({difficulty}) - {xp_reward} XP")
    
    def view_quests(self, filter_type=None):
        """Display all active quests."""
        print("\n=== ACTIVE QUESTS ===")
        
        active_quests = self.quests["active"]
        if filter_type:
            active_quests = [q for q in active_quests if q["type"] == filter_type]
        
        if not active_quests:
            print("No active quests. Create one to start your adventure!")
            return
        
        for idx, quest in enumerate(active_quests, 1):
            icon = {"main": "⚔️", "side": "📜", "daily": "🔄"}.get(quest["type"], "📝")
            print(f"\n{idx}. {icon} {quest['title']}")
            print(f"   Difficulty: {quest['difficulty']} | Reward: {quest['xp_reward']} XP")
            print(f"   Type: {quest['type'].title()} | Skill: {quest['skill'].title()}")
            if quest['description']:
                print(f"   Description: {quest['description']}")
        
        print(f"\n📊 Total Active Quests: {len(active_quests)}")
    
    def view_completed_quests(self):
        """Display all completed quests."""
        print("\n=== COMPLETED QUESTS ===")
        
        if not self.quests["completed"]:
            print("No completed quests yet. Complete your first quest to start your legend!")
            return
        
        for idx, quest in enumerate(self.quests["completed"], 1):
            icon = {"main": "⚔️", "side": "📜", "daily": "🔄"}.get(quest["type"], "📝")
            completed_date = quest['completed_at'][:10] if quest.get('completed_at') else "Unknown"
            print(f"\n{idx}. {icon} {quest['title']} ✅")
            print(f"   Difficulty: {quest['difficulty']} | XP Earned: {quest['xp_reward']}")
            print(f"   Completed: {completed_date}")
            if quest['description']:
                print(f"   Description: {quest['description']}")
        
        print(f"\n📊 Total Quests Completed: {len(self.quests['completed'])}")
    
    def complete_quest(self):
        """Mark a quest as completed."""
        self.view_quests()
        
        if not self.quests["active"]:
            return
        
        try:
            choice = int(input("\nEnter quest number to complete (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.quests["active"]):
                quest = self.quests["active"][choice - 1]
                quest["status"] = "completed"
                quest["completed_at"] = datetime.now().isoformat()
                
                # Award XP
                xp_gained = quest["xp_reward"]
                self.add_xp(xp_gained)
                
                # Add skill XP
                skill = quest["skill"]
                self.player["skills"][skill] += xp_gained // 10
                
                # Move to completed
                self.quests["active"].pop(choice - 1)
                self.quests["completed"].append(quest)
                
                # Update stats
                self.player["quests_completed"] += 1
                
                # Check for achievements
                self.check_achievements()
                
                self.save_all()
                
                print(f"\n✅ Quest completed: '{quest['title']}'")
                print(f"💎 Gained {xp_gained} XP!")
                print(f"📈 {skill.title()} skill increased!")
            else:
                print("Invalid quest number!")
        except ValueError:
            print("Please enter a valid number!")
    
    def check_achievements(self):
        """Check if player has earned any new achievements."""
        achievements = []
        
        # First quest
        if self.player["quests_completed"] == 1 and "First Steps" not in self.player["achievements"]:
            achievements.append("First Steps")
        
        # 10 quests
        if self.player["quests_completed"] == 10 and "Adventurer" not in self.player["achievements"]:
            achievements.append("Adventurer")
        
        # 50 quests
        if self.player["quests_completed"] == 50 and "Hero" not in self.player["achievements"]:
            achievements.append("Hero")
        
        # Reach level 5
        if self.player["level"] >= 5 and "Rising Star" not in self.player["achievements"]:
            achievements.append("Rising Star")
        
        # Display new achievements
        for achievement in achievements:
            print(f"\n🏆 ACHIEVEMENT UNLOCKED: {achievement}! 🏆")
            self.player["achievements"].append(achievement)
    
    def view_character(self):
        """Display player character sheet."""
        print("\n" + "="*50)
        print("CHARACTER SHEET".center(50))
        print("="*50)
        
        print(f"\n👤 Name: {self.player['name']}")
        print(f"⭐ Level: {self.player['level']}")
        
        # XP Progress bar
        current_xp = self.player['xp']
        needed_xp = self.calculate_xp_for_level(self.player['level'])
        progress = int((current_xp / needed_xp) * 20)
        bar = "█" * progress + "░" * (20 - progress)
        print(f"💎 XP: [{bar}] {current_xp}/{needed_xp}")
        
        print(f"\n📊 Total XP Earned: {self.player['total_xp']}")
        print(f"✅ Quests Completed: {self.player['quests_completed']}")
        
        print("\n🎯 Skills:")
        for skill, value in self.player['skills'].items():
            skill_bar = "▰" * (value // 20) + "▱" * (5 - (value // 20))
            print(f"   {skill.title():<15} [{skill_bar}] {value}")
        
        if self.player['achievements']:
            print("\n🏆 Achievements:")
            for achievement in self.player['achievements']:
                print(f"   • {achievement}")
        
        print("\n" + "="*50)
    
    def add_note(self):
        """Add a note to knowledge base."""
        print("\n=== ADD KNOWLEDGE NOTE ===")
        title = input("Note Title: ").strip()
        if not title:
            print("Note title cannot be empty!")
            return
        
        content = input("Note Content: ").strip()
        tags = input("Tags (comma-separated): ").strip().split(",")
        tags = [tag.strip() for tag in tags if tag.strip()]
        
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
    
    def simple_chat(self):
        """Simple chat interface (no AI for prototype)."""
        print("\n=== QUEST ADVISOR ===")
        print("(Prototype version - AI integration coming soon!)")
        print("\nAvailable commands:")
        print("  'stats' - Show your character stats")
        print("  'suggest' - Get quest suggestions")
        print("  'knowledge' - Search knowledge base")
        print("  'exit' - Return to main menu")
        
        while True:
            user_input = input("\nYou: ").strip().lower()
            
            if user_input == "exit":
                break
            elif user_input == "stats":
                self.view_character()
            elif user_input == "suggest":
                print("\nAdvisor: Based on your progress, here are some suggestions:")
                print("• Create a Daily Quest for consistent habits")
                print("• Try a Medium difficulty quest to level up faster")
                print(f"• Focus on your '{min(self.player['skills'], key=self.player['skills'].get)}' skill")
            elif user_input == "knowledge":
                self.view_notes()
            else:
                print("\nAdvisor: I don't understand that command yet. Try 'stats', 'suggest', or 'knowledge'.")
    
    def main_menu(self):
        """Display main menu and handle user input."""
        while True:
            print("\n" + "="*50)
            print("⚔️  QUEST LOG - Your Adventure Awaits!  ⚔️".center(50))
            print("="*50)
            print(f"\nLevel {self.player['level']} {self.player['name']} | {self.player['xp']} XP")
            print(f"Active Quests: {len(self.quests['active'])} | Completed: {self.player['quests_completed']}")
            
            print("\n1. 📜 View Active Quests")
            print("2. ✨ Create Quest")
            print("3. ✅ Complete Quest")
            print("4. 📋 View Completed Quests")
            print("5. 👤 Character Sheet")
            print("6. 📝 Add Knowledge Note")
            print("7. 📚 View Knowledge Base")
            print("8. 💬 Chat with Quest Advisor")
            print("9. 🚪 Exit")
            
            choice = input("\nChoose an option: ").strip()
            
            if choice == "1":
                self.view_quests()
            elif choice == "2":
                self.create_quest()
            elif choice == "3":
                self.complete_quest()
            elif choice == "4":
                self.view_completed_quests()
            elif choice == "5":
                self.view_character()
            elif choice == "6":
                self.add_note()
            elif choice == "7":
                self.view_notes()
            elif choice == "8":
                self.simple_chat()
            elif choice == "9":
                print("\n⚔️  Your progress has been saved. Until next time, adventurer! ⚔️\n")
                break
            else:
                print("\n❌ Invalid option! Please choose 1-9.")


def main():
    """Entry point for the application."""
    print("\n" + "="*50)
    print("⚔️  QUEST LOG - PROTOTYPE v1  ⚔️".center(50))
    print("="*50)
    print("\nWelcome to Quest Log - Your Gamified Task Manager!")
    print("Turn your tasks into epic quests and level up in real life.\n")
    
    app = QuestLog()
    
    # First-time setup
    if app.player["total_xp"] == 0:
        name = input("Enter your adventurer name: ").strip()
        if name:
            app.player["name"] = name
            app.save_all()
        
        print(f"\nWelcome, {app.player['name']}! Your journey begins now.")
        print("Create your first quest to start earning XP and leveling up!")
    
    app.main_menu()


if __name__ == "__main__":
    main()