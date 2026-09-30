"""
Task 2: Tic-Tac-Toe AI

The AI uses the Minimax algorithm, with optional Alpha-Beta pruning,
to play perfectly: it never loses (the best a human can get is a draw).

Board: a list of 9 cells, index 0..8 (left to right, top to bottom)
    0 | 1 | 2
    3 | 4 | 5
    6 | 7 | 8

Run in terminal:   python tictactoe.py
Run the web UI:    streamlit run app.py
"""

import math

EMPTY = " "
HUMAN = "X"
AI = "O"

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


# --------------------------------------------------------------------------
# Game rules
# --------------------------------------------------------------------------
def winner(board):
    """Return 'X' or 'O' if someone has won, else None."""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return EMPTY not in board


def game_over(board):
    return winner(board) is not None or is_full(board)


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]


# --------------------------------------------------------------------------
# Minimax (with optional Alpha-Beta pruning)
# --------------------------------------------------------------------------
def minimax(board, depth, is_ai_turn, alpha, beta, use_pruning, counter):
    """
    Returns the score of the position from the AI's point of view:
      AI wins    -> positive (higher if the win is faster)
      Human wins -> negative (less negative if the loss is slower)
      Draw       -> 0
    `counter` is a one-item list used to count how many positions were explored.
    """
    counter[0] += 1

    w = winner(board)
    if w == AI:
        return 10 - depth
    if w == HUMAN:
        return depth - 10
    if is_full(board):
        return 0

    if is_ai_turn:  # AI maximizes the score
        best = -math.inf
        for move in available_moves(board):
            board[move] = AI
            score = minimax(board, depth + 1, False, alpha, beta, use_pruning, counter)
            board[move] = EMPTY
            best = max(best, score)
            if use_pruning:
                alpha = max(alpha, best)
                if beta <= alpha:  # the human would never allow this branch
                    break
        return best
    else:  # Human minimizes the score
        best = math.inf
        for move in available_moves(board):
            board[move] = HUMAN
            score = minimax(board, depth + 1, True, alpha, beta, use_pruning, counter)
            board[move] = EMPTY
            best = min(best, score)
            if use_pruning:
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best


def best_move(board, use_pruning=True):
    """
    Pick the best move for the AI.
    Returns (move_index, positions_explored).
    """
    board = board[:]  # work on a copy
    counter = [0]
    best_score = -math.inf
    move_chosen = None

    for move in available_moves(board):
        board[move] = AI
        score = minimax(board, 1, False, -math.inf, math.inf, use_pruning, counter)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            move_chosen = move

    return move_chosen, counter[0]


# --------------------------------------------------------------------------
# Terminal game
# --------------------------------------------------------------------------
def print_board(board):
    print()
    for r in range(3):
        print(" " + " | ".join(board[r * 3: r * 3 + 3]))
        if r < 2:
            print("---+---+---")
    print()


def main():
    print("Tic-Tac-Toe AI  (you are X, AI is O)")
    print("Enter a cell number 1-9:\n 1 | 2 | 3\n---+---+---\n 4 | 5 | 6\n---+---+---\n 7 | 8 | 9")

    board = [EMPTY] * 9
    ai_first = input("\nShould the AI go first? (y/n): ").strip().lower() == "y"
    if ai_first:
        move, _ = best_move(board)
        board[move] = AI

    while True:
        print_board(board)
        if game_over(board):
            break

        try:
            cell = int(input("Your move (1-9): ")) - 1
        except ValueError:
            print("Please enter a number from 1 to 9.")
            continue
        if cell not in range(9) or board[cell] != EMPTY:
            print("That cell is not available. Try another one.")
            continue

        board[cell] = HUMAN
        if game_over(board):
            print_board(board)
            break

        move, nodes = best_move(board)
        board[move] = AI
        print(f"AI played {move + 1} (explored {nodes} positions)")

    w = winner(board)
    if w == AI:
        print("AI wins! Better luck next time.")
    elif w == HUMAN:
        print("You win!")
    else:
        print("It's a draw.")


if __name__ == "__main__":
    main()