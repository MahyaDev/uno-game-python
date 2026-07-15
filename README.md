# UNO Game

A Python implementation of the UNO card game using Object-Oriented Programming (OOP) principles.

## About the Project

This project is a console-based implementation of the classic UNO card game in Python.
It is being developed incrementally, with the game logic implemented first before adding a graphical user interface.

## Project Structure

```text
uno/
├── card.py
├── deck.py
├── player.py
└── game.py
```

## Current Features

### Card Module
- Card representation
- Card colors and values
- Number, Action, and Wild cards
- Card validation
- Playability rules

### Deck Module
- Standard UNO deck generation
- Deck shuffling
- Drawing cards
- Discard pile management
- Recycling the discard pile

### Player Module
- Hand management
- Drawing and playing cards
- Playable card detection
- Color selection for Wild cards
- UNO call support

### Game Module
- Turn management
- Player rotation
- Direction handling
- Card effect processing
  - Skip
  - Reverse
  - Draw Two
  - Wild
  - Wild Draw Four
- Win detection

## Technologies

- Python 3
- Object-Oriented Programming (OOP)

## Future Plans

- Computer-controlled player
- Console interface improvements
- Graphical User Interface (GUI)
- Additional game features and polishing

## Project Status

🚧 Work in progress
