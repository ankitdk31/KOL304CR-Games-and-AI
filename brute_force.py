import itertools

def find_winner(state):
    """Check the board and return the winner symbol if any."""
    win_patterns = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # Vertical
        (0, 4, 8), (2, 4, 6)               # Diagonal
    ]

    for x, y, z in win_patterns:
        if state[x] == state[y] == state[z] and state[x] != " ":
            return state[x]  # 'X' or 'O'
    return None

def open_positions(state):
    """Return the indexes of empty cells."""
    return [idx for idx, cell in enumerate(state) if cell == " "]

def optimal_move_search(state, current):
    """
    Use brute-force search to find the most favorable move
    by evaluating all possible future game states.
    """
    best_choice = None
    highest_score = -float('inf')
    opponent = "O" if current == "X" else "X"

    for option in open_positions(state):
        test_board = state[:]
        test_board[option] = current

        # If this move immediately wins the game
        if find_winner(test_board) == current:
            return option

        # Check opponent responses
        possible_enemy_moves = open_positions(test_board)
        if not possible_enemy_moves:
            score = 0  # Board full → draw
        else:
            worst_outcome = float('inf')
            for enemy in possible_enemy_moves:
                scenario = test_board[:]
                scenario[enemy] = opponent

                if find_winner(scenario) == opponent:
                    worst_outcome = -1  # Losing scenario
                    break
                worst_outcome = min(worst_outcome, 0)

            score = -worst_outcome

        if score > highest_score:
            highest_score = score
            best_choice = option

    return best_choice

# Example usage
board_state = [
    "X", "O", "X",
    " ", "O", " ",
    " ", " ", "X"
]

move = optimal_move_search(board_state, "O")
print(f"Recommended move for 'O': {move}")
