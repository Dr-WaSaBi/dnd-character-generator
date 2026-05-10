# D&D 5e Character Generator

A desktop character sheet builder for Dungeons & Dragons 5th Edition, built with Python and PyQt6.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![PyQt6](https://img.shields.io/badge/PyQt6-6.11%2B-green) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Features

- **Parchment-themed UI** — dark wood frame with a scrollable parchment character sheet
- **10 interactive sections** — click any numbered section to open its editor
- **Save / Load** — characters persist as `.dnd5e` files (plain JSON) so you can quit and come back
- **Sections completed so far:**
  | # | Section | Notes |
  |---|---------|-------|
  | 1 | Character Info | Name, class, level, race, background, alignment, XP, player name |
  | 2 | Ability Scores | Roll 4d6-drop-lowest, Standard Array, or Point Buy (27 pts) |
  | 3 | Saving Throws | Auto-applies class proficiencies; manually overridable |
  | 4–10 | *(coming soon)* | Skills, combat stats, attacks, equipment, personality, features, proficiencies |

---

## Requirements

- Python **3.10 or newer**
- Windows, macOS, or Linux with a desktop environment

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/Dr-WaSaBi/dnd-character-generator.git
cd dnd-character-generator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

| Platform | Command |
|----------|---------|
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the app

```bash
python main.py
```

> **Windows shortcut:** after activating the venv you can also run `.venv\Scripts\python.exe main.py`

---

## Usage

### Opening the app

The main window shows a D&D 5e character sheet divided into 10 numbered sections. Each section is a clickable card. Hover over a card to highlight it, then click to open its editor.

### Building a character — recommended order

1. **Section 1 — Character Info** — fill in your character's name, class, level, race, background, alignment, and XP first. Class and level feed into other sections automatically.
2. **Section 2 — Ability Scores** — choose a method and assign your six core stats:
   - 🎲 **Roll 4d6 (drop lowest)** — roll six values, then drag-assign them to abilities
   - 📋 **Standard Array** — pick from the fixed set [15, 14, 13, 12, 10, 8]
   - 🧮 **Point Buy** — spend 27 points using the official cost table (scores 8–15)
3. **Section 3 — Saving Throws** — your class's two proficiencies are auto-applied based on Section 1. Toggle any proficiency on/off to override.
4. Sections 4–10 are under active development.

### Saving your character

| Action | Shortcut | Notes |
|--------|----------|-------|
| Save | `Ctrl+S` | Saves to the current file; prompts for a path on first save |
| Save As | `Ctrl+Shift+S` | Always prompts for a new file path |
| Open | `Ctrl+O` | Load a previously saved `.dnd5e` file |
| New | `Ctrl+N` | Clear the sheet and start fresh (warns if you have unsaved data) |

Character files use the `.dnd5e` extension and are plain JSON — you can open them in any text editor.

---

## Project structure

```
dnd-character-generator/
├── main.py                      # Entry point
├── requirements.txt
├── assets/                      # Images, icons (future use)
├── data/                        # Static game data (future use)
└── ui/
    ├── character_sheet.py       # Main window + section card layout
    ├── styles.py                # Shared colors and fonts
    └── editors/
        ├── character_info.py    # Section 1 editor
        ├── ability_scores.py    # Section 2 editor
        └── saving_throws.py     # Section 3 editor
```

---

## Contributing

Pull requests are welcome. Please open an issue first to discuss larger changes.

---

## License

MIT
