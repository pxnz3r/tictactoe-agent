# tictactoe-agent

AI Lab coursework: a tic-tac-toe agent with game-tree search: minimax, alpha-beta pruning and a depth-limited heuristic evaluation.

## Layout

- `tictactoe_agent/` this project's code: `game.py` (board and rules), `agents.py` (the searches and agents), `report.py` (which outputs make up the results)
- `pxlab/` vendored copy of the shared engine (see `pxlab/VERSION`). Don't edit it here; it is replaced on the next sync.
- `main.py` runs the full study and rewrites `docs/results.md`; `app.py` is the Streamlit demo; `app_overview.md` the demo's Overview text
- `outputs/` figures and CSV tables (committed for the hosted app)
- `docs/` methodology, results, deploy

## Commands

- Full study: `uv run python main.py`
- Demo: `uv run streamlit run app.py`
- Lint: `uv run ruff check . && uv run ruff format --check .`

## Conventions

- Beginner-student style on purpose: plain functions, docstrings on every function, comments explaining the AI concepts.
- Seed 42 for the tournament.
- After changing the study, re-run `main.py` and refresh the README results and `app_overview.md`.
