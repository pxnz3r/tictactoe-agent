"""
agents.py - game-tree search for tic-tac-toe.

The game tree has the current board at its root, a branch for every legal
move and a leaf for every finished game. The agents search it depth-first:
down one line of play to the end, back up, then the next.

    minimax: X picks the move with the highest value, O the lowest,
        assuming both play their best. Searching the whole tree gives
        perfect play.
    alpha-beta pruning: the same answer as minimax, but skips branches
        that can't change it.
    depth-limited minimax with a heuristic: look only a few moves ahead
        and score the boards there with a rule of thumb.

Values are from X's point of view: positive is good for X, negative for O,
0 a draw. A win is worth 100 plus the empty cells left, so a faster win
scores higher and a slower loss less badly.
"""

from dataclasses import dataclass
from functools import cache

import numpy as np

from tictactoe_agent.game import EMPTY, LINES, START, is_over, legal_moves, play, to_move, winner

WIN = 100

# Cells tried first by move ordering: centre, corners, then edges. Strong
# moves first make alpha-beta prune sooner.
GOOD_ORDER = [4, 0, 2, 6, 8, 1, 3, 5, 7]


@dataclass
class Counter:
    """Counts the boards a search visits."""

    nodes: int = 0


def final_score(board):
    """
    The value of a finished game.

    Input:
        board: a finished board.
    Returns:
        WIN + empty cells for an X win, minus that for an O win, 0 for a draw.
    """
    champion = winner(board)
    if champion is None:
        return 0
    bonus = WIN + board.count(EMPTY)
    return bonus if champion == "X" else -bonus


def minimax(board, counter):
    """
    Plain minimax: search every move to the end of the game.

    Inputs:
        board: the board to value.
        counter: a Counter, increased once per board visited.
    Returns:
        The value of the board with perfect play from here.
    """
    counter.nodes += 1
    if is_over(board):
        return final_score(board)
    values = [minimax(play(board, cell), counter) for cell in legal_moves(board)]
    return max(values) if to_move(board) == "X" else min(values)


def alpha_beta(board, counter, alpha=-np.inf, beta=np.inf, ordered=False):
    """
    Minimax with alpha-beta pruning.

    alpha is the best value X is already sure of elsewhere in the tree,
    beta the best O is sure of. Once a branch is proven worse for the
    player choosing it than what they already have (alpha >= beta), the
    rest of its moves can't matter and are skipped.

    Inputs:
        board: the board to value.
        counter: a Counter, increased once per board visited.
        alpha, beta: the bounds described above.
        ordered: True to try centre and corners before edges.
    Returns:
        The same value as minimax().
    """
    counter.nodes += 1
    if is_over(board):
        return final_score(board)
    moves = legal_moves(board)
    if ordered:
        moves = sorted(moves, key=GOOD_ORDER.index)
    if to_move(board) == "X":
        best = -np.inf
        for cell in moves:
            best = max(best, alpha_beta(play(board, cell), counter, alpha, beta, ordered))
            alpha = max(alpha, best)
            if alpha >= beta:
                break  # O would never let the game reach this board
        return best
    best = np.inf
    for cell in moves:
        best = min(best, alpha_beta(play(board, cell), counter, alpha, beta, ordered))
        beta = min(beta, best)
        if alpha >= beta:
            break  # X would never let the game reach this board
    return best


def heuristic(board):
    """
    A rule of thumb for an unfinished board, from X's point of view.

    Each of the eight lines still open to only one player counts for that
    player: 1 point with one of their marks in it, 10 with two. A line
    with both players' marks can never win and counts for nothing.

    Input:
        board: an unfinished board.
    Returns:
        X's points minus O's points.
    """
    score = 0
    for line in LINES:
        marks = [board[cell] for cell in line]
        x, o = marks.count("X"), marks.count("O")
        if o == 0 and x:
            score += 10 ** (x - 1)
        elif x == 0 and o:
            score -= 10 ** (o - 1)
    return score


def depth_limited(board, depth, counter):
    """
    Minimax that looks only `depth` moves ahead and scores the boards
    there with heuristic().

    Inputs:
        board: the board to value.
        depth: moves left to look ahead.
        counter: a Counter, increased once per board visited.
    Returns:
        The estimated value.
    """
    counter.nodes += 1
    if is_over(board):
        return final_score(board)
    if depth == 0:
        return heuristic(board)
    values = [depth_limited(play(board, cell), depth - 1, counter) for cell in legal_moves(board)]
    return max(values) if to_move(board) == "X" else min(values)


@cache
def perfect_value(board):
    """
    The minimax value of a board, remembered once worked out. There are
    only 5,478 boards reachable in a real game, so the perfect agent
    stays instant.

    Input:
        board: a board tuple.
    Returns:
        The value with perfect play.
    """
    if is_over(board):
        return final_score(board)
    values = [perfect_value(play(board, cell)) for cell in legal_moves(board)]
    return max(values) if to_move(board) == "X" else min(values)


# Agent name -> how far it looks ahead (None means to the end of the game).
AGENTS = {
    "Random": 0,
    "Heuristic, 1 move ahead": 1,
    "Heuristic, 2 moves ahead": 2,
    "Heuristic, 4 moves ahead": 4,
    "Perfect (minimax)": None,
}


def move_values(board, agent):
    """
    The value the agent gives every legal move.

    Inputs:
        board: the board, with the agent to move.
        agent: a key of AGENTS other than "Random".
    Returns:
        Dictionary cell -> value from X's point of view.
    """
    depth = AGENTS[agent]
    values = {}
    for cell in legal_moves(board):
        after = play(board, cell)
        if depth is None:
            values[cell] = perfect_value(after)
        else:
            values[cell] = depth_limited(after, depth - 1, Counter())
    return values


def choose_move(board, agent, generator):
    """
    The agent's move. Ties between equally valued moves are broken at
    random, so games vary.

    Inputs:
        board: the board, with the agent to move.
        agent: a key of AGENTS.
        generator: a numpy random generator.
    Returns:
        A cell number.
    """
    moves = legal_moves(board)
    if agent == "Random":
        return int(moves[generator.integers(len(moves))])
    values = move_values(board, agent)
    best = max(values.values()) if to_move(board) == "X" else min(values.values())
    candidates = [cell for cell, value in values.items() if value == best]
    return int(candidates[generator.integers(len(candidates))])


def play_game(x_agent, o_agent, generator):
    """
    One game between two agents.

    Inputs:
        x_agent, o_agent: keys of AGENTS.
        generator: a numpy random generator.
    Returns:
        "X", "O" or None for a draw.
    """
    board = START
    while not is_over(board):
        agent = x_agent if to_move(board) == "X" else o_agent
        board = play(board, choose_move(board, agent, generator))
    return winner(board)
