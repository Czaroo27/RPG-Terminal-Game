# 🧙‍♂️ Text-Based RPG Game

A simple terminal-based RPG game written in Python. Explore a randomly generated map, fight enemies, collect treasures, level up, and manage your inventory.

## 🎮 Features

- 💾 Save & Load system (`rpg_save.json`)
- 🗺️ Randomly generated 10x10 map
- ⚔️ Turn-based combat system with enemies (Goblin, Orc, Dragon)
- 💎 Treasure events with items and gold
- 📦 Inventory system (use potions and power-ups)
- ⬆️ Leveling system with stat growth
- 🎲 Random events and encounters

## 🚀 Getting Started

### Requirements

- Python 3.x

### Running the Game

```bash
python main.py
```

### Menu

When launching the game, you'll be prompted with:

```
1. New Game
2. Load Game
```

## 🎮 Controls

- `w` - move up
- `s` - move down
- `a` - move left
- `d` - move right
- `i` - open inventory
- `q` - save and quit

## 🧾 Game Mechanics

### Map Symbols

- `P` — Player
- `.` — Empty space
- `E` — Enemy
- `T` — Treasure

### Combat

- Attack or attempt to flee during battles.
- Defeating enemies grants experience and gold.
- Leveling up increases stats (HP, Mana, Strength, Defense).

### Inventory

- Use healing or strength potions.
- Each item has an effect (e.g. healing 30 HP or boosting strength).

## 📂 Save File

The game automatically saves to `rpg_save.json` and includes:

- Player stats and inventory
- Current map layout
- Player's position

## 📌 Notes

- Treasures may contain gold or useful items.
- Random events add atmosphere and variety.
- Game ends when the player's HP reaches 0.

## 🛠️ Future Ideas

- Add spell system (mana-based attacks)
- Introduce shops and NPCs
- Implement quest or story system
- Add more enemies, items, and status effects

---

Made with ❤️ in Python
