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

The project uses an inheritance hierarchy beginning with `DijitalVarlik`. `SiberSavasci`, `KodAvcisi`, `AgFedaisi`, and `Virus` model the player and enemy entities. Character-specific `ozel_guc()` implementations demonstrate method overriding and polymorphic behavior. The game also uses constructors, `super()`, instance attributes, methods, and type hints on core classes and functions.

## Requirements

- Python 3.8 or later
- No third-party packages required (Python standard library only)

## Run

```bash
python siber_savas.py
```

Run the command in a terminal. The game is interactive and requires keyboard input.

## Tests

The project includes a regression suite using Python's built-in `unittest` framework. It covers health and damage boundaries, character abilities, defense damage, enemy scaling, boss generation, and input validation.

Run the tests from the project root. GitHub Actions also runs the suite on pushes and pull requests for Python 3.8, 3.11, and 3.12:

```bash
python -m unittest discover -s tests -v
```

## Maintenance note

This began as a student project and is being maintained incrementally as a portfolio exercise. Recent changes add regression tests, type hints, and input validation while intentionally preserving the original gameplay and scope.

## Controls

During combat:

- `1` — Attack
- `2` — Defend
- `3` — Use special ability

Invalid menu entries are rejected and the prompt is repeated; an invalid combat command no longer gives the enemy a free turn.

At the end of a level, enter `e` to continue or `h` to exit. Other inputs are rejected and the prompt is repeated.

## Project structure

```text
siber-savas-rpg/
├── README.md
├── .gitignore
├── siber_savas.py
├── tests/
│   └── test_game_logic.py
└── .github/
    └── workflows/
        └── python-tests.yml
```

## Project context

This is a learning project created to practice Python and object-oriented programming through a small command-line game. It is not a cybersecurity tool and does not perform network operations or interact with real malware.
