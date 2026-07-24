# UNO Game

A Python implementation of the classic UNO card game using Object-Oriented Programming (OOP) principles.

## About the Project

This project is a console-based implementation of the classic UNO card game in Python.
The core mechanics of the game are fully playable through a command-line interface, with the code organized using OOP principles.
A graphical user interface (GUI) may be added in the future.

## Project Structure

```text
.
├── main.py
└── uno/
    ├── card.py
    ├── deck.py
    ├── player.py
    └── game.py
```

## Current Features

### Card System
- Card representation
- Number, Action, and Wild cards
- Card colors and values
- Card validation
- Playability rules

### Deck Management
- Standard 108-card UNO deck generation
- Deck shuffling
- Drawing cards
- Discard pile management
- Automatic discard pile recycling

### Players
- Human player
- Heuristic-based AI bot player
- Hand management
- Drawing and playing cards
- Strategic Wild card color selection
- UNO call support

### Bot Strategy

The AI bot selects playable cards using a heuristic scoring system instead of choosing randomly.

Current decision factors include:

- Card type
- Color and value matching
- Dominant color in hand
- Duplicate cards
- Late-game Wild card usage

### Game Logic
- Turn management
- Polymorphic player system
- Player rotation
- Reverse direction
- Skip turns
- Draw Two
- Wild
- Wild Draw Four
- Win detection

### Command-Line Interface
- Interactive game setup
- Configurable number of bot opponents
- Random starting player
- Play again option
- Gameplay feedback in the terminal

## Technologies

- Python 3
- Object-Oriented Programming (OOP)

## Learning Goals

This project is part of my learning journey to improve my skills in:

- Object-Oriented Programming (OOP)
- Python
- Software design
- Heuristic algorithms
- Git and GitHub workflow

## Future Plans

- Context-aware bot strategy
- Improved console interface
- Graphical User Interface (GUI)
- Additional UNO rules and game modes
- Save game statistics

## Project Status

🚧 Work in progress
