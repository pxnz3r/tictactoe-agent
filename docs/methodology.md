# Methodology

## Question

How does an agent choose good moves in a two-player game by searching ahead, how much of the game tree does each search need, and how good are the moves it finds?

## The game tree

A board is a tuple of 9 cells, each "X", "O" or empty, read row by row. X moves first; whose turn it is follows from the count of marks. The game ends when a player fills one of the 8 lines (3 rows, 3 columns, 2 diagonals) or the board is full.

The game tree has the current board at its root, one branch per legal move and a leaf for every finished game. Every search here walks it depth-first: one line of play to the end, back up, then the next.

Values are from X's point of view. A finished game is worth 100 plus the number of empty cells for an X win, minus that for an O win, and 0 for a draw. The bonus for empty cells makes a faster win worth more and a slower loss less bad, so the agents win quickly and resist longest when lost.

## The searches

| Search | How it values a board | Exact? |
| --- | --- | --- |
| Minimax | Searches every continuation to the end. X takes the highest value of its moves, O the lowest. | Yes |
| Alpha-beta | Minimax, but keeps the best value each side is already sure of (alpha for X, beta for O). Once alpha >= beta, the remaining moves at that board can't change the result and are skipped. | Yes, same value as minimax |
| Alpha-beta, ordered | Alpha-beta that tries the centre, then corners, then edges. Strong moves first make the cut-offs come sooner. | Yes |
| Depth-limited, heuristic | Minimax that stops after 1, 2 or 4 moves and scores the unfinished boards there. | No, an estimate |

The heuristic counts lines still open to only one player: 1 point with one of their marks in it, 10 with two. A line holding both players' marks can never be won and counts for nothing. The score is X's points minus O's.

The perfect agent caches the minimax value of each board it has worked out (there are only 5,478 reachable boards), so it plays instantly.

## The agents

Five agents: Random (any empty cell), the heuristic searching 1, 2 and 4 moves ahead, and Perfect (full minimax). Each picks the move with the best value; ties between equally valued moves are broken at random, so games vary.

## Measurements

1. **Tree size**: every board in the full tree counted with repeats, complete games counted, and distinct boards counted.
2. **Search effort**: boards visited and time taken by each search to value two positions, the empty board and "X in a corner, O in the centre". Counts don't depend on the machine; times are from one run in plain Python and only comparable with each other.
3. **Tournament**: every agent against every agent (itself included), 100 games as X and 100 as O, seed 42. Results are wins, draws and losses for the first-named agent, and points per game (win 1, draw 0.5).

## Limits

Tic-tac-toe is small enough to solve completely, which is what makes the exact searches comparable with the estimates. On larger games (chess, Go) a full search is impossible, so only depth-limited search with a heuristic, plus pruning and move ordering, stays practical.
