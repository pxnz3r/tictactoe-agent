"""
app.py - play tic-tac-toe against the agents. Run it with:

    streamlit run app.py

Tabs:
    Overview      how game-tree search works and what was found,
    Play          play against an agent and see how it valued each move,
    Search effort how much of the game tree each search visits,
    Results       the saved tables and figures from main.py.
"""

import numpy as np
import pandas as pd
import streamlit as st

from pxlab.app import setup_page, show_figure, show_markdown_file, show_results_tabs, show_table
from tictactoe_agent.agents import AGENTS, WIN, choose_move, move_values
from tictactoe_agent.game import EMPTY, START, is_over, play, to_move, winner
from tictactoe_agent.report import FOLDER, results_sections

PERFECT = "Perfect (minimax)"


def new_game():
    """
    Reset the board, and let the agent open if it plays X.

    Returns:
        Nothing.
    """
    st.session_state.board = START
    st.session_state.last_values = None
    if st.session_state.human == "O":
        agent_moves()


def agent_moves():
    """
    The agent picks its move and remembers how it valued every option.

    Returns:
        Nothing.
    """
    board = st.session_state.board
    agent = st.session_state.agent
    if agent != "Random":
        st.session_state.last_values = (board, move_values(board, agent))
    else:
        st.session_state.last_values = None
    st.session_state.board = play(board, choose_move(board, agent, st.session_state.generator))


def human_moves(cell):
    """
    Take the player's move, then the agent replies.

    Input:
        cell: the cell clicked.
    Returns:
        Nothing.
    """
    st.session_state.board = play(st.session_state.board, cell)
    if not is_over(st.session_state.board):
        agent_moves()


def value_label(value, agent_mark, agent):
    """
    A move's value in words, from the agent's side.

    Inputs:
        value: the value from X's point of view.
        agent_mark: "X" or "O", the agent's side.
        agent: the agent's name.
    Returns:
        A short string.
    """
    mine = value if agent_mark == "X" else -value
    if abs(mine) > WIN:
        last_move = 9 - (abs(mine) - WIN)  # the win bonus counts the empty cells left
        return f"{'win' if mine > 0 else 'loss'} by move {last_move}"
    if agent == PERFECT:
        return "draw"
    return f"{mine:+.0f}"


def show_board():
    """
    The board as a 3x3 grid of buttons; empty cells are clickable on the
    player's turn.

    Returns:
        Nothing.
    """
    board = st.session_state.board
    playing = not is_over(board) and to_move(board) == st.session_state.human
    for row in range(3):
        columns = st.columns(3, gap="small")
        for column in range(3):
            cell = row * 3 + column
            columns[column].button(
                board[cell] if board[cell] != EMPTY else " ",
                key=f"cell-{cell}",
                on_click=human_moves,
                args=(cell,),
                disabled=not (playing and board[cell] == EMPTY),
                width="stretch",
            )


def show_play_page():
    """
    The Play tab.

    Returns:
        Nothing.
    """
    if "board" not in st.session_state:
        st.session_state.generator = np.random.default_rng()
        st.session_state.human = "X"
        st.session_state.agent = PERFECT
        new_game()

    side_box, agent_box, button_box = st.columns([2, 3, 2], vertical_alignment="bottom")
    side_box.radio("You play", ["X", "O"], key="human", horizontal=True, on_change=new_game, help="X moves first.")
    agent_box.selectbox("Opponent", list(AGENTS), key="agent", on_change=new_game)
    button_box.button("New game", on_click=new_game, width="stretch")

    left, right = st.columns([2, 3], gap="large")
    with left:
        show_board()
        board = st.session_state.board
        if is_over(board):
            champion = winner(board)
            if champion is None:
                st.subheader("Draw", anchor=False)
            else:
                st.subheader("You win" if champion == st.session_state.human else "The agent wins", anchor=False)
    with right:
        last = st.session_state.last_values
        if last is None:
            if st.session_state.agent == "Random":
                st.markdown("The random agent picks any empty cell, so there is nothing to explain.")
            else:
                st.markdown("Make a move. After the agent replies, its value for every option shows here.")
            return
        before, values = last
        agent_mark = to_move(before)
        st.markdown(f"**How the agent valued its options** (it plays {agent_mark})")
        grid = [[before[r * 3 + c] if before[r * 3 + c] != EMPTY else "" for c in range(3)] for r in range(3)]
        for cell, value in values.items():
            grid[cell // 3][cell % 3] = value_label(value, agent_mark, st.session_state.agent)
        st.table(pd.DataFrame(grid, columns=["", " ", "  "]))
        if st.session_state.agent == PERFECT:
            st.caption(
                "Minimax searched every possible continuation, assuming you play perfectly too. "
                "It picks a win if there is one, else a draw, at random among equals."
            )
        else:
            st.caption(
                f"It looked {AGENTS[st.session_state.agent]} move(s) ahead and scored the boards there: each line "
                "still open to it adds 1 point per mark (10 for two), each line open only to you subtracts the same."
            )


def show_effort_page():
    """
    The Search effort tab.

    Returns:
        Nothing.
    """
    st.markdown(
        "Tic-tac-toe's game tree from the empty board holds 549,946 boards: 255,168 complete games. "
        "Plain minimax visits all of them to choose the first move. Alpha-beta pruning skips branches that "
        "can't change the answer and visits 20,866; trying the centre and corners first (strong moves first) "
        "makes the cuts come sooner, 7,865. A depth-limited search with a heuristic visits only a few "
        "thousand boards, but its value is an estimate."
    )
    show_figure(f"{FOLDER}/search_effort.png")
    show_table("Boards visited to value a position", f"{FOLDER}/search_effort.csv")


def main():
    """
    Build the page.

    Returns:
        Nothing.
    """
    setup_page("Tic-tac-toe agent")
    overview, game, effort, results = st.tabs(["Overview", "Play", "Search effort", "Results"])
    with overview:
        show_markdown_file("app_overview.md")
    with game:
        show_play_page()
    with effort:
        show_effort_page()
    with results:
        show_results_tabs(results_sections())


main()
