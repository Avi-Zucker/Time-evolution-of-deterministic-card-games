# Time-evolution-of-deterministic-card-games

# Overview
This project simulates a deterministic card game using Python. It includes:

A script that implements the rules and logic of a two-player deterministic card game using a standard deck.

A second script that runs multiple simulations of the game and collects statistics, such as the number of turns until the game ends.

The goal is to explore deterministic behavior in card games and analyze how initial conditions affect game length.

# Motivation
Card games are usually associated with randomness. However, if both players follow strict deterministic rules and the deck order is fixed, the game outcome becomes predictable. This project demonstrates that concept, using Python to simulate and analyze such games.

It is useful for understanding how deterministic systems Time-evolution depened on the intial condition.

# Files
game_<name>.py — runs a single deterministic game

analyze.py — runs many games and collects statistics

# Example Use Cases
Analyze the distribution number of turns until a game ends

Detect looping behavior

Compare different games

# Requirements
Python 3.8+

Standard library only (unless extended)

# How to Download and use
Clone the repository using git

git clone https://github.com/Avi-Zucker/deterministic-card-game.git
cd deterministic-card-game

run
python game.py <game_name>

<game_name> is the name of the game to simulate (e.g., war, Hearts)





this project is part of the [Puthon course](https://github.com/Code-Maven/wis-python-course-2025-03?tab=readme-ov-file) by [Gábor Szabó](https://github.com/szabgab)
