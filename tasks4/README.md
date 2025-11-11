# Task 4 - OpenAI API Task Summarizer

A command-line application that uses OpenAI's GPT-4o-mini to automatically summarize paragraph-length task descriptions into short phrases.

## Features

- Connects to OpenAI Chat Completions API
- Summarizes multiple task descriptions
- Loops through tasks independently
- Includes sample task paragraphs

## Setup

1. **Install dependencies:**
```bash
   uv add openai python-dotenv
```

2. **Create `.env` file with your API key:**
```
   OPENAI_API_KEY=your-openai-key-here
```

3. **Add `.env` to `.gitignore`:**
```bash
   echo ".env" >> .gitignore
```

## Running
```bash
uv run python main.py
```

## Sample Output
```
Task 1:
Description: I need to prepare a comprehensive presentation...
✨ Summary: Prepare CSC299 AI presentation
```

## Files

- `main.py` - Application code
- `.env` - API key (not in git)
- `pyproject.toml` - Package config

## Security

API key stored in `.env` and excluded from version control.