# Quest Log - Gamified Task Manager

A command-line task management system with RPG mechanics that turns your daily tasks into epic quests. Level up, earn XP, unlock achievements, and track your progress as you complete real-life tasks!

## Features

- **Task Management**: Create, list, complete, and search tasks (quests)
- **RPG Mechanics**: Earn XP, level up, and develop skills
- **Quest Types**: Main quests (big goals), side quests (optional tasks), daily quests (habits)
- **Difficulty Levels**: Trivial, Easy, Medium, Hard, Epic (with corresponding XP rewards)
- **Achievement System**: Unlock achievements as you progress
- **Knowledge Base**: Store notes and build your personal knowledge management system
- **JSON Storage**: All data stored in human-readable JSON files
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/csc299-project.git
cd csc299-project/tasks1
```

2. No additional installation needed! All required libraries are part of Python's standard library.

## Running the Application

### Basic Usage

```bash
python quest_log.py
```

Or make it executable (Linux/Mac):
```bash
chmod +x quest_log.py
./quest_log.py
```

### First Time Setup

When you run the application for the first time, you'll be prompted to enter your adventurer name. This creates your character profile.

## Usage Guide

### Main Menu Options

```
1. 📜 View Active Quests    - Display all your current tasks
2. ✨ Create Quest          - Add a new task/quest
3. ✅ Complete Quest        - Mark a quest as done and earn XP
4. 📋 View Completed Quests - See your quest history
5. 🔍 Search Quests         - Search through all quests
6. 👤 Character Sheet       - View your stats, level, and skills
7. 📝 Add Knowledge Note    - Store notes in your knowledge base
8. 📚 View Knowledge Base   - View all your saved notes
9. 💬 Chat with Quest Advisor - Interactive help system
10. 🚪 Exit                 - Save and exit the application
```

### Creating a Quest

When creating a quest, you'll specify:

1. **Title**: Name your quest
2. **Description**: Describe what needs to be done
3. **Difficulty**: Choose from 5 levels
   - Trivial (10 XP)
   - Easy (25 XP)
   - Medium (50 XP)
   - Hard (100 XP)
   - Epic (250 XP)
4. **Type**: Select quest category
   - Main Quest (big goals)
   - Side Quest (optional tasks)
   - Daily Quest (routine habits)
5. **Skill**: Choose primary skill
   - Productivity
   - Learning
   - Health
   - Creativity

### Searching Quests

The search feature allows you to find quests by:
- Title keywords
- Description text
- Quest type (main, side, daily)
- Difficulty level
- Associated skill

Search works across both active and completed quests.

### Leveling System

- Start at Level 1 with 0 XP
- XP required per level increases exponentially: `100 × (1.5^(level-1))`
- Complete quests to earn XP
- Level up automatically when you have enough XP
- Each level unlocks more potential!

### Skills

Four skills track your progress in different areas:
- **Productivity**: Work and task completion
- **Learning**: Education and skill development
- **Health**: Physical and mental wellness
- **Creativity**: Creative projects and hobbies

Skills increase based on the quests you complete (10% of quest XP goes to the associated skill).

### Achievements

Unlock achievements by reaching milestones:
- **First Steps**: Complete your first quest
- **Adventurer**: Complete 10 quests
- **Hero**: Complete 50 quests
- **Rising Star**: Reach level 5
- More achievements to discover!

## Data Storage

All data is stored in the `data/` directory in JSON format:

```
tasks1/
├── quest_log.py
├── README.md
└── data/
    ├── player.json      # Your character stats
    ├── quests.json      # All quests (active & completed)
    └── knowledge.json   # Your knowledge base notes
```

### Data Files

**player.json** - Contains your character information:
- Name, level, XP
- Skills progress
- Achievements earned
- Quest completion stats

**quests.json** - Contains all your quests:
- Active quests (current tasks)
- Completed quests (quest history)
- Quest templates (future feature)

**knowledge.json** - Contains your notes:
- Notes with titles and content
- Tags for organization
- Timestamps for tracking

### Backing Up Your Data

Simply copy the entire `data/` folder to back up your progress:

```bash
cp -r data/ data_backup/
```

## Examples

### Example 1: Creating Your First Quest

```
Choose an option: 2

=== CREATE NEW QUEST ===
Quest Title: Finish CSC299 homework
Description: Complete the coding assignment for class
Choose difficulty (1-5): 3
Choose type (1-3): 1
Choose skill (1-4): 2

✨ Quest created: 'Finish CSC299 homework' (Medium) - 50 XP
```

### Example 2: Completing a Quest

```
Choose an option: 3

=== ACTIVE QUESTS ===
1. ⚔️ Finish CSC299 homework
   Difficulty: Medium | Reward: 50 XP
   Type: Main | Skill: Learning
   
Enter quest number to complete (0 to cancel): 1

✅ Quest completed: 'Finish CSC299 homework'
💎 Gained 50 XP!
📈 Learning skill increased!
```

### Example 3: Searching for Quests

```
Choose an option: 5

=== SEARCH QUESTS ===
Enter search term: homework

🔍 Found 1 quest(s) matching 'homework':

✅ ⚔️ Finish CSC299 homework
   Status: COMPLETED | Type: Main | Difficulty: Medium
   Reward: 50 XP | Skill: Learning
```

### Example 4: Viewing Character Progress

```
Choose an option: 6

==================================================
              CHARACTER SHEET
==================================================

👤 Name: Alex
⭐ Level: 2
💎 XP: [████████░░░░░░░░░░░░] 45/150

📊 Total XP Earned: 195
✅ Quests Completed: 5

🎯 Skills:
   Productivity    [▰▰▱▱▱] 42
   Learning        [▰▰▰▱▱] 68
   Health          [▰▱▱▱▱] 15
   Creativity      [▰▱▱▱▱] 20

🏆 Achievements:
   • First Steps
```

## Tips for Success

1. **Start Small**: Begin with Daily Quests to build consistency
2. **Balance Difficulty**: Mix easy and hard quests for steady progress
3. **Track Everything**: Use the knowledge base to store important information
4. **Review Progress**: Check your Character Sheet regularly to see growth
5. **Set Main Quests**: Use Main Quests for big, important goals
6. **Daily Habits**: Create Daily Quests for recurring activities
7. **Celebrate Wins**: Watch for achievement unlocks and level ups!

## Troubleshooting

### Data Not Saving
- Ensure the `data/` directory has write permissions
- Check that you're exiting through the menu (option 10) to trigger save

### JSON Errors
- If data files become corrupted, delete the `data/` folder and restart
- The application will create fresh data files automatically

### Character Not Found
- First-time users need to create a character by entering a name
- If you deleted `player.json`, you'll need to start over

## Future Enhancements

Planned features for future versions:
- AI-powered quest suggestions using LLM integration
- Better terminal UI with colors and formatting (Rich library)
- Quest scheduling and deadlines
- Recurring daily quests with auto-regeneration
- Data export/import functionality
- Quest templates for reusable task patterns
- Streak tracking for consistency
- More achievement types

## Contributing

This is a student project for CSC299. Feedback and suggestions are welcome!

## License

Created as part of CSC299 coursework.

---

**Happy Questing! May your tasks be epic and your XP plentiful! ⚔️**
