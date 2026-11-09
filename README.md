# Siber Savaş: Bit Yolu

A terminal-based, turn-based RPG written in Python. Choose a cyber warrior, fight progressively stronger malware enemies, and try to survive as long as possible.

## Gameplay

- Choose one of two character classes:
  - **Kod Avcısı (Code Hunter):** Higher attack damage and an Overclock ability that deals double damage.
  - **Ağ Fedaisi (Network Defender):** Higher health and a Patch ability that restores health.
- Fight enemies using attack, defense, and special abilities.
- Enemy strength and health scale with the current level.
- A ransomware boss appears every five levels.
- Restore some health after each successful encounter and decide whether to continue to the next level.

## Object-oriented programming concepts

The project uses an inheritance hierarchy beginning with `DijitalVarlik`. `SiberSavasci`, `KodAvcisi`, `AgFedaisi`, and `Virus` model the player and enemy entities. Character-specific `ozel_guc()` implementations demonstrate method overriding and polymorphic behavior. The game also uses constructors, `super()`, instance attributes, and methods.

## Requirements

- Python 3.8 or later
- No third-party packages required (Python standard library only)

## Run

```bash
python siber_savas.py
```

Run the command in a terminal. The game is interactive and requires keyboard input.

## Controls

During combat:

- `1` — Attack
- `2` — Defend
- `3` — Use special ability

At the end of a level, enter `e` to continue to the next sector. Any other response exits the game.

## Project structure

```text
siber-savas-rpg/
├── README.md
├── .gitignore
└── siber_savas.py
```

## Project context

This is a learning project created to practice Python and object-oriented programming through a small command-line game. It is not a cybersecurity tool and does not perform network operations or interact with real malware.
