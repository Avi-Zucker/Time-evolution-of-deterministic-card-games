from common import create_shuffled_deck, check_loop

def war_game_ver1():
    
    """
    Simulates the card game 'War' between two players, Version 1.

    Game Rules (Version 1):
    1. A standard deck of 52 cards is shuffled and split evenly between two players.
    2. Each player plays their top card. The higher card wins both cards.
    3. In case of a tie ('war'):
       - Each player places three face-down cards and one face-up card.
       - The higher face-up card wins the entire pile.
       - If another tie occurs, the process repeats.
       - (in Version 1) If a player has fewer than four cards during a war, the game immediately ends.
    4. The game ends if one player collects all the cards or if a loop is detected.

    
    Loop Detection:
    - The game records each unique game state.
    - If a state repeats, a loop is detected and the game stops.

    Output:
        The number of steps (rounds) taken until the game ends.
        Note: face dwon cards during a war does not count as a step
        The reason for ending: "Player wins" or "Loop detected"
    """
   
    player1, player2 = create_shuffled_deck()

    steps = 0
    seen_states = set()

    while player1 and player2:
        steps += 1

        # Save current state and check for a loop
        current_state = (tuple(player1), tuple(player2))
        if check_loop(current_state, seen_states):
            return steps, 'Loop detected'

        card1 = player1.popleft()
        card2 = player2.popleft()

        if card1 > card2:
            player1.extend([card1, card2])
        elif card2 > card1:
            player2.extend([card2, card1])
        else:
            # War situation
            pile = [card1, card2]

            while True:
                if len(player1) < 4 or len(player2) < 4:
                    # Game ends because a player cannot continue the war
                    print(f"Game ended after {steps} steps. A player ran out of cards during war.")
                    return steps

                # Each player places 3 face-down and 1 face-up card
                pile.extend([player1.popleft() for _ in range(3)])
                pile.extend([player2.popleft() for _ in range(3)])

                card1 = player1.popleft()
                card2 = player2.popleft()
                pile.extend([card1, card2])

                steps += 1

                if card1 > card2:
                    player1.extend(pile)
                    break
                elif card2 > card1:
                    player2.extend(pile)
                    break
                # If tie again, repeat war

                # if both players ran out of cards and the pile is tie
                if not player1 and not player2:
                    print(f"Game ended after {steps} steps. Both players ran out of cards.")
                    return steps

    print(f"Game ended after {steps} steps. One player has all the cards.")
    return steps

# Example run
if __name__ == "__main__":
    steps = war_game_ver1()

