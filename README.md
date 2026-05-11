# PyGame Dungeon

A simple PyGame project template.

## Setup Instructions

### 1. Create a Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Game

```bash
python main.py
```

### 4. Deactivate Virtual Environment

When you're done working on the project:
```bash
deactivate
```

## Project Structure

```
pygame-dungeon/
├── assets/           # Game assets
│   ├── images/      # Sprites, backgrounds, etc.
│   ├── sounds/      # Sound effects and music
│   └── fonts/       # Custom fonts
├── src/             # Game source code
│   ├── __init__.py
│   └── game.py      # Main game class
├── main.py          # Entry point
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Requirements

- Python 3.8 or higher
- PyGame 2.6.0
