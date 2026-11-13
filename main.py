"""
main.py - run the whole tic-tac-toe study with one command:

    python main.py

It:
    1. measures the game tree: every possible game, every distinct board,
    2. counts the boards each search visits to pick a move: plain minimax,
       alpha-beta pruning (with and without move ordering) and
       depth-limited search with the heuristic,
    3. plays a tournament between the agents, 200 games per pairing, each
       side playing X in half of them,
    4. writes docs/results.md.
Figures and tables go to outputs/tictactoe/.
"""

import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from pxlab.common import RANDOM_STATE, save_figure, save_table, set_plot_style, write_results_doc
from tictactoe_agent.agents import (
    AGENTS,
    Counter,
    alpha_beta,
    depth_limited,
    minimax,
    perfect_value,
    play_game,
)
from tictactoe_agent.game import START, is_over, legal_moves, play
from tictactoe_agent.report import FOLDER, results_sections

GAMES_PER_SIDE = 100

# Positions to search from: the empty board, and X in a corner with O in
# the centre (X to move).
POSITIONS = {
    "Empty board": START,
    "X corner, O centre": play(play(START, 0), 4),
}


def count_games(board):
    """
    Count every complete game that can follow a board (the leaves of the
    game tree).

    Input:
        board: a board tuple.
    Returns:
        The number of finished games.
    """
    if is_over(board):
        return 1
    return sum(count_games(play(board, cell)) for cell in legal_moves(board))


def tree_size():
    """
    The size of the whole game tree from the empty board.

    Returns:
        A one-column table of counts.
    """
    counter = Counter()
    value = minimax(START, counter)
    perfect_value.cache_clear()
    perfect_value(START)
    rows = {
        "Boards in the full game tree (with repeats)": counter.nodes,
        "Complete games": count_games(START),
        "Distinct boards": perfect_value.cache_info().currsize,
        "Value of the empty board with perfect play": value,
    }
    table = pd.DataFrame({"Count": rows})
    save_table(table, f"{FOLDER}/tree_size.csv", index=True)
    print(table.to_string())
    return table


def search_effort():
    """
    Boards visited and time taken by each search to value a position.

    Returns:
        The table.
    """
    searches = {
        "Minimax (full tree)": lambda board, counter: minimax(board, counter),
        "Alpha-beta": lambda board, counter: alpha_beta(board, counter),
        "Alpha-beta, centre and corners first": lambda board, counter: alpha_beta(board, counter, ordered=True),
        "Heuristic, 1 move ahead": lambda board, counter: depth_limited(board, 1, counter),
        "Heuristic, 2 moves ahead": lambda board, counter: depth_limited(board, 2, counter),
        "Heuristic, 4 moves ahead": lambda board, counter: depth_limited(board, 4, counter),
    }
    rows = []
    for position, board in POSITIONS.items():
        for name, search in searches.items():
            counter = Counter()
            started = time.perf_counter()
            value = search(board, counter)
            rows.append(
                {
                    "Position": position,
                    "Search": name,
                    "Boards visited": counter.nodes,
                    "Milliseconds": round((time.perf_counter() - started) * 1000, 1),
                    "Value": value,
                }
            )
    table = pd.DataFrame(rows)
    save_table(table, f"{FOLDER}/search_effort.csv")
    print(table.to_string(index=False))

    figure, axis = plt.subplots(figsize=(9, 4.8))
    pivot = table.pivot(index="Search", columns="Position", values="Boards visited").loc[list(searches)]
    pivot.plot.barh(ax=axis, logx=True)
    axis.invert_yaxis()
    axis.set_xlabel("Boards visited (log scale)")
    axis.set_ylabel("")
    axis.set_title("How much of the game tree each search visits")
    save_figure(figure, f"{FOLDER}/search_effort.png")
    return table


def wilson_interval(count, total, z=1.96):
    """
    95% Wilson interval for a rate such as losses / games. Unlike the
    plain rate +- 2 standard errors, it stays inside 0 to 1 and still gives
    a useful upper bound when the count is 0 ("never lost in 200 games"
    means the true loss rate is probably below about 2%).

    Inputs:
        count: how many times it happened.
        total: how many games.
        z: 1.96 for 95%.
    Returns:
        (low, high).
    """
    rate = count / total
    centre = (rate + z**2 / (2 * total)) / (1 + z**2 / total)
    spread = z * np.sqrt(rate * (1 - rate) / total + z**2 / (4 * total**2)) / (1 + z**2 / total)
    return max(0.0, centre - spread), min(1.0, centre + spread)


def tournament():
    """
    Every agent against every agent, 100 games as X and 100 as O.

    Returns:
        The results table.
    """
    generator = np.random.default_rng(RANDOM_STATE)
    names = list(AGENTS)
    rows = []
    for agent in names:
        for opponent in names:
            wins = draws = losses = 0
            for agent_mark, pairing in [("X", (agent, opponent)), ("O", (opponent, agent))]:
                for _ in range(GAMES_PER_SIDE):
                    result = play_game(*pairing, generator)
                    if result is None:
                        draws += 1
                    elif result == agent_mark:
                        wins += 1
                    else:
                        losses += 1
            low, high = wilson_interval(losses, 2 * GAMES_PER_SIDE)
            rows.append(
                {
                    "Agent": agent,
                    "Opponent": opponent,
                    "Wins": wins,
                    "Draws": draws,
                    "Losses": losses,
                    "Loss rate, 95% interval": f"{low:.1%} to {high:.1%}",
                }
            )
        print(f"  {agent}: done")
    table = pd.DataFrame(rows)
    save_table(table, f"{FOLDER}/tournament.csv")

    points = table.assign(Points=(table["Wins"] + 0.5 * table["Draws"]) / (2 * GAMES_PER_SIDE))
    grid = points.pivot(index="Agent", columns="Opponent", values="Points").loc[names, names]
    figure, axis = plt.subplots(figsize=(8.5, 6))
    sns.heatmap(grid, annot=True, fmt=".2f", cmap="RdYlGn", vmin=0, vmax=1, ax=axis, cbar_kws={"label": "Points"})
    axis.set_title("Points per game for the row agent (win 1, draw 0.5, loss 0)")
    axis.set_xlabel("Opponent")
    axis.set_ylabel("Agent")
    save_figure(figure, f"{FOLDER}/tournament.png")
    return table


def main():
    """
    The full study.

    Returns:
        Nothing.
    """
    set_plot_style()
    print("Game tree:")
    tree_size()
    print("Search effort:")
    search_effort()
    print("Tournament:")
    tournament()
    write_results_doc(
        "Results",
        "Produced by `python main.py`. Counts don't depend on the machine; times are from one run in plain "
        "Python. Tournament ties between equally good moves are broken at random with seed 42.",
        results_sections(),
    )
    print("  Done. Run: streamlit run app.py")


if __name__ == "__main__":
    main()
