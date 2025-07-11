# Time evolution of deterministic card games

# Overview
This project simulates a deterministic card game using Python.

It includes:

for each Game a script that inplements the game with a random deck of cards, the script run the game
              according to its specific rules until the game ends, and determines how many turns the gamr                 lasts.

A second script runs multiple simulations of the game and collects from each game the number of turns until the game ends, and plut the outcome.              

The type of the games is deterministic - games where the players dont make any decisions during the game

(e.g., [war](https://en.wikipedia.org/wiki/War_(card_game)), 
[Beggar-my-neighbour](https://en.wikipedia.org/wiki/Beggar-my-neighbour)).


The goal is to explore deterministic behavior in card games and analyze how initial conditions affect game length.

# Motivation

Card games are usually associated with randomness. However, if both players follow strict deterministic rules and the deck order is fixed, the game outcome becomes predictable. This project demonstrates that concept, using Python to simulate and analyze such games.

It is useful for understanding how deterministic systems Time-evolution depened on the intial condition.

# Files
- Game files - runs a single deterministic game
- `War_ver1.py`
- `War_ver2.py`
- `begger_my_neighbour.py`
- simulation — runs multiple games and collects statistics
- `Game_Simulator.py`

# Example Use Cases
- Analyze the distribution number of turns until a game ends
- Detect looping behavior
- Compare different games, or different versions of the same game

# Requirements
Python 3.8+

Standard library only (unless extended)

# How to Download and use
Clone the repository using git:

```bash
git clone https://github.com/Avi-Zucker/deterministic-card-game.git
cd deterministic-card-game
```

run one Game
```bash
python <game_name>.py
```

run simulation
```bash
python Game_Simulator.py
```

# Credit
this project is part of the [Python course](https://github.com/Code-Maven/wis-python-course-2025-03?tab=readme-ov-file) by [Gábor Szabó](https://github.com/szabgab)
