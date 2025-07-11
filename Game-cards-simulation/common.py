from collections import deque
import random
import numpy as np
from scipy.stats import expon
import matplotlib.pyplot as plt

def create_shuffled_deck():
    """
    Creates a shuffled standard deck and splits it evenly between two players.
    Returns:
        player1, player2: deque of cards (each 26 cards)
    """
    deck = list(range(2, 15)) * 4  # Cards 2 to 14 (Ace high)
    random.shuffle(deck)
    player1 = deque(deck[:26]) 
    player2 = deque(deck[26:]) 
    return player1, player2


def check_loop(current_state, seen_states):
    """
    Detects if the current game state has occurred before.
    Args:
        current_state (tuple): Current state of the game (deck1, deck2).
        seen_states (set): Set of previously seen states.
    Returns:
        bool: True if a loop is detected.
    """
    if current_state in seen_states:
        return True
    seen_states.add(current_state)
    return False

def switch_player(current_player):
    """
    Switches between player 1 and player 2.
    Args:
        current_player (int): Current player's turn (1 or 2).
    Returns:
        int: The other player's number.
    """
    return 2 if current_player == 1 else 1


def run_simulation_batch(game_func, batch_size):
    """
    Runs a batch of game simulations.
    Args:
        game_func (callable): The function that runs a single game.
        batch_size (int): Number of games to run in this batch.
    Returns:
        list of int: Steps taken for each game.
    """
    results = []
    for _ in range(batch_size):
        result = game_func()
        steps = result[0] if isinstance(result, tuple) else result
        results.append(steps)
    return results

def fit_exponential_tail(data, threshold=None):
    """
    Fits an exponential distribution to the tail of the simulation data.
    Args:
        data (list of int): List of durations (steps) from games.
        threshold (float, optional): Start of the tail. If None, peak bin is used.
    Returns:
        tuple: x_fit (X values for fit curve),
               y_fit (Y values for fit curve),
               lambda (1/scale of fitted exponential),
               mean of data,
               number of samples
    """
    if not data:
        raise ValueError("Input data is empty.")

    if threshold is None:
        counts, bins = np.histogram(data, bins=100)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        max_index = np.argmax(counts)
        threshold = bin_centers[max_index]

    tail_data = [x for x in data if x >= threshold]
    if not tail_data:
        raise ValueError("Tail data is empty; cannot fit.")

    loc, scale = expon.fit(tail_data, floc=0)
    x_fit = np.linspace(threshold, max(data), 500)
    y_fit = expon.pdf(x_fit, loc=loc, scale=scale) * len(tail_data) * (x_fit[1] - x_fit[0])

    return x_fit, y_fit, 1/scale, np.mean(data), len(data)