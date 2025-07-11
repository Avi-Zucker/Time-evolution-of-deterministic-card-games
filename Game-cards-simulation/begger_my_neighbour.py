from collections import deque
from common import create_shuffled_deck, check_loop

def play_beggar_my_neighbour():
    
    """
    Simulates the card game 'Beggar-my-Neighbour'.

    Game Rules:
    1. A standard deck of 52 cards is shuffled and split evenly between two players.
    2. Players take turns playing the top card from their deck to a central pile.
    3. If a player plays a face card (J, Q, K, A):
       - The opponent must play a penalty of 1 card for Jack, 2 for Queen, 3 for King, 4 for Ace.
       - If a face card appears during the penalty, the penalty resets and the other player must pay.
       - If the penalty is completed without another face card appearing, the player who played the face card wins the pile.
    4. The game continues until one player has all the cards or a previous state repeats (loop detection).

    Returns:
        The number of steps (turns) until the game ends.

    """

    player1, player2 = create_shuffled_deck()

    steps = 0
    seen_states = set()

    pile = deque()
    player_turn = 1  # 1 or 2

    penalty_count = 0
    penalty_owner = None

    while player1 and player2:
        steps += 1

        # Save current state and check for a loop
        current_state = (tuple(player1), tuple(player2))
        if check_loop(current_state, seen_states):
            return steps, 'Loop detected'

        if player_turn == 1:
            if not player1:
                return steps
            card = player1.popleft()
        else:
            if not player2:
                return steps
            card = player2.popleft()

        pile.append(card)

        if card >= 11:  # Face card played
            penalty_count = {11: 1, 12: 2, 13: 3, 14: 4}[card]
            penalty_owner = player_turn
            player_turn = 2 if player_turn == 1 else 1
            continue

        if penalty_count > 0:
            penalty_count -= 1

            if penalty_count == 0:
                if penalty_owner == 1:
                    player1.extend(pile)
                else:
                    player2.extend(pile)
                pile.clear()
                penalty_owner = None
        else:
            player_turn = 2 if player_turn == 1 else 1

    print(f"Game ended after {steps} steps. One player has all the cards.")
    return steps

if __name__ == "__main__":
    steps = play_beggar_my_neighbour()
