### What this is

A tic-tac-toe agent that chooses its moves by searching the **game tree**: the current board at the root, a branch for every legal move, a leaf for every finished game. It searches depth-first, following one line of play to the end before trying the next.

Five agents are compared:

- **Perfect (minimax)**: searches every continuation to the end. It assumes both sides play their best: X picks the highest value, O the lowest.
- **Heuristic, 1, 2 or 4 moves ahead**: searches only that deep, then scores the board with a rule of thumb (each line still open to one player counts for them, more with two marks in it).
- **Random**: any empty cell.

### What to try

- **Play**: take X or O against any agent. After each reply, see how the agent valued every option.
- **Search effort**: how much of the tree each search visits.
- **Results**: the tree's size and the full tournament.

### What was found

- **The full tree has 549,946 boards** (255,168 complete games, 5,478 distinct boards). Perfect play from both sides is a draw.
- **Alpha-beta pruning visits 26 times fewer boards** than plain minimax for the first move (20,866), and 70 times fewer (7,865) when it tries the centre and corners first, with the same answer.
- **Looking 2 moves ahead is already enough** here: that heuristic agent never lost a game, not even to perfect play. Looking 1 move ahead lost 37 of 200 games to perfect play.
- **Perfect isn't the best against a weak player.** Minimax won 86% of its games against the random agent; the 1-move heuristic won 96%. Against the 1-move heuristic, minimax won 16% and the 2-move heuristic 25%. Minimax assumes a perfect opponent, so every move that keeps the draw looks equal to it, even one that gives a weak opponent no way to go wrong. The heuristic prefers boards with more open lines, which sets more traps.

Code and every figure: [github.com/pxnz3r/tictactoe-agent](https://github.com/pxnz3r/tictactoe-agent).
