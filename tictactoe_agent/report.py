"""
report.py - which saved tables and figures make up the results. The app's
Results tab and docs/results.md both read this list, so they always match.
"""

FOLDER = "tictactoe"


def results_sections():
    """
    The results, grouped into sections.

    Returns:
        A list of (section name, items) for pxlab's show_results_tabs() and
        write_results_doc().
    """
    return [
        ("Game tree", [("table", "Size of the tic-tac-toe game tree", f"{FOLDER}/tree_size.csv")]),
        (
            "Search effort",
            [
                ("figure", f"{FOLDER}/search_effort.png"),
                ("table", "Boards visited to value a position", f"{FOLDER}/search_effort.csv"),
            ],
        ),
        (
            "Tournament",
            [
                ("figure", f"{FOLDER}/tournament.png"),
                ("table", "200 games per pairing, results for the first-named agent", f"{FOLDER}/tournament.csv"),
            ],
        ),
    ]
