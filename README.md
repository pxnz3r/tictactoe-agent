# Tic-tac-toe agent

A tic-tac-toe agent that picks its moves by searching the game tree: plain minimax, minimax with alpha-beta pruning, and a depth-limited search that scores unfinished boards with a heuristic. A tournament pits every agent against every other, and an interactive demo lets you play them and see how they valued each move.

![Points per game for each agent against each opponent](outputs/figures/tictactoe/tournament.png)

## Results

| Question | Finding |
| --- | --- |
| How big is the game tree? | 549,946 boards from the empty board, 255,168 complete games, 5,478 distinct boards. Perfect play from both sides is a draw. |
| What does alpha-beta save? | The same first-move value from 20,866 boards instead of 549,946 (26x fewer), and 7,865 (70x fewer) when it tries the centre and corners first. |
| How far must a heuristic agent look? | 2 moves ahead never lost a game, even to perfect play. 1 move ahead lost 37 of 200 games to it. |
| Is perfect play the best play? | Not against weak players. Minimax won 86% against the random agent, the 1-move heuristic 96%. Minimax treats every move that keeps the draw as equal; the heuristic prefers boards with more open lines, which sets more traps. |

**Boards visited to value the empty board:**

| Search | Boards visited | Milliseconds |
| --- | --- | --- |
| Minimax (full tree) | 549,946 | 2,316 |
| Alpha-beta | 20,866 | 110 |
| Alpha-beta, centre and corners first | 7,865 | 40 |
| Heuristic, 2 moves ahead | 82 | 0.7 |
| Heuristic, 4 moves ahead | 3,610 | 30 |

Full tables and figures: [docs/results.md](docs/results.md). How it was done: [docs/methodology.md](docs/methodology.md).

## Run it

Needs Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python main.py
uv run streamlit run app.py
```

`main.py` counts the game tree, measures each search and runs the tournament, writing figures and tables to `outputs/` and `docs/results.md`. The demo plays live and needs `main.py`'s output only for the Search effort and Results tabs.

## The demo

- **Overview**: the agents and what was found.
- **Play**: play X or O against any agent. After each reply, a grid shows the value the agent gave every empty cell.
- **Search effort**: boards visited by each search.
- **Results**: the tree size, search effort and tournament tables.

## Layout

```
tictactoe_agent/   game.py (board and rules), agents.py (minimax, alpha-beta, heuristic search), report.py
pxlab/             shared engine (vendored): app and output helpers
main.py            the full study
app.py             the Streamlit demo
docs/              methodology, results, deploy
```

## License

MIT.
