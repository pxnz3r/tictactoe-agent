"""
game.py - the rules of tic-tac-toe.

A board is a tuple of 9 cells read row by row, each "X", "O" or " ".
Cells are numbered 0 to 8:

    0 | 1 | 2
    3 | 4 | 5
    6 | 7 | 8

X always moves first.
"""

EMPTY = " "
START = (EMPTY,) * 9

# The eight lines that win: three rows, three columns, two diagonals.
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def other(player):
    """The opponent of "X" is "O" and the other way round."""
    return "O" if player == "X" else "X"


def to_move(board):
    """
    Whose turn it is: X when both have played the same number of times.

    Input:
        board: a board tuple.
    Returns:
        "X" or "O".
    """
    return "X" if board.count("X") == board.count("O") else "O"


def winner(board):
    """
    The player with three in a line, if any.

    Input:
        board: a board tuple.
    Returns:
        "X", "O" or None.
    """
    for a, b, c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def legal_moves(board):
    """
    The empty cells, if the game isn't over.

    Input:
        board: a board tuple.
    Returns:
        A list of cell numbers.
    """
    if winner(board):
        return []
    return [cell for cell in range(9) if board[cell] == EMPTY]


def is_over(board):
    """True when someone has won or the board is full."""
    return winner(board) is not None or EMPTY not in board


def play(board, cell):
    """
    The board after the player to move takes a cell.

    Inputs:
        board: a board tuple.
        cell: an empty cell number.
    Returns:
        A new board tuple.
    """
    cells = list(board)
    cells[cell] = to_move(board)
    return tuple(cells)
