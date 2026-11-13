# Results

Produced by `python main.py`. Counts don't depend on the machine; times are from one run in plain Python. Tournament ties between equally good moves are broken at random with seed 42.

## Game tree

### Size of the tic-tac-toe game tree

|  | Count |
| --- | --- |
| Boards in the full game tree (with repeats) | 549946 |
| Complete games | 255168 |
| Distinct boards | 5478 |
| Value of the empty board with perfect play | 0 |

## Search effort

![search effort](../outputs/figures/tictactoe/search_effort.png)

### Boards visited to value a position

| Position | Search | Boards visited | Milliseconds | Value |
| --- | --- | --- | --- | --- |
| Empty board | Minimax (full tree) | 549946 | 2221.2 | 0 |
| Empty board | Alpha-beta | 20866 | 107.7 | 0 |
| Empty board | Alpha-beta, centre and corners first | 7865 | 29.5 | 0 |
| Empty board | Heuristic, 1 move ahead | 10 | 0.1 | 4 |
| Empty board | Heuristic, 2 moves ahead | 82 | 0.4 | 1 |
| Empty board | Heuristic, 4 moves ahead | 3610 | 16.8 | 0 |
| X corner, O centre | Minimax (full tree) | 7332 | 36.0 | 0 |
| X corner, O centre | Alpha-beta | 871 | 2.7 | 0 |
| X corner, O centre | Alpha-beta, centre and corners first | 768 | 2.6 | 0 |
| X corner, O centre | Heuristic, 1 move ahead | 8 | 0.0 | 10 |
| X corner, O centre | Heuristic, 2 moves ahead | 50 | 0.2 | -9 |
| X corner, O centre | Heuristic, 4 moves ahead | 1020 | 4.2 | -8 |

## Tournament

![tournament](../outputs/figures/tictactoe/tournament.png)

### 200 games per pairing, results for the first-named agent

| Agent | Opponent | Wins | Draws | Losses | Loss rate, 95% interval |
| --- | --- | --- | --- | --- | --- |
| Random | Random | 86 | 31 | 83 | 34.9% to 48.4% |
| Random | Heuristic, 1 move ahead | 4 | 10 | 186 | 88.6% to 95.8% |
| Random | Heuristic, 2 moves ahead | 0 | 18 | 182 | 86.2% to 94.2% |
| Random | Heuristic, 4 moves ahead | 0 | 17 | 183 | 86.8% to 94.6% |
| Random | Perfect (minimax) | 0 | 15 | 185 | 88.0% to 95.4% |
| Heuristic, 1 move ahead | Random | 192 | 4 | 4 | 0.8% to 5.0% |
| Heuristic, 1 move ahead | Heuristic, 1 move ahead | 0 | 200 | 0 | 0.0% to 1.9% |
| Heuristic, 1 move ahead | Heuristic, 2 moves ahead | 0 | 156 | 44 | 16.8% to 28.2% |
| Heuristic, 1 move ahead | Heuristic, 4 moves ahead | 0 | 169 | 31 | 11.1% to 21.2% |
| Heuristic, 1 move ahead | Perfect (minimax) | 0 | 163 | 37 | 13.7% to 24.5% |
| Heuristic, 2 moves ahead | Random | 184 | 16 | 0 | 0.0% to 1.9% |
| Heuristic, 2 moves ahead | Heuristic, 1 move ahead | 50 | 150 | 0 | 0.0% to 1.9% |
| Heuristic, 2 moves ahead | Heuristic, 2 moves ahead | 0 | 200 | 0 | 0.0% to 1.9% |
| Heuristic, 2 moves ahead | Heuristic, 4 moves ahead | 0 | 200 | 0 | 0.0% to 1.9% |
| Heuristic, 2 moves ahead | Perfect (minimax) | 0 | 200 | 0 | 0.0% to 1.9% |
| Heuristic, 4 moves ahead | Random | 179 | 21 | 0 | 0.0% to 1.9% |
| Heuristic, 4 moves ahead | Heuristic, 1 move ahead | 33 | 167 | 0 | 0.0% to 1.9% |
| Heuristic, 4 moves ahead | Heuristic, 2 moves ahead | 0 | 200 | 0 | 0.0% to 1.9% |
| Heuristic, 4 moves ahead | Heuristic, 4 moves ahead | 0 | 200 | 0 | 0.0% to 1.9% |
| Heuristic, 4 moves ahead | Perfect (minimax) | 0 | 200 | 0 | 0.0% to 1.9% |
| Perfect (minimax) | Random | 172 | 28 | 0 | 0.0% to 1.9% |
| Perfect (minimax) | Heuristic, 1 move ahead | 31 | 169 | 0 | 0.0% to 1.9% |
| Perfect (minimax) | Heuristic, 2 moves ahead | 0 | 200 | 0 | 0.0% to 1.9% |
| Perfect (minimax) | Heuristic, 4 moves ahead | 0 | 200 | 0 | 0.0% to 1.9% |
| Perfect (minimax) | Perfect (minimax) | 0 | 200 | 0 | 0.0% to 1.9% |
