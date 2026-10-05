"""Mill detection for Morris board positions."""

from morris.board.constants import EMPTY
from morris.board.representation import is_valid_board


MILL_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (8, 9, 10),
    (11, 12, 13),
    (14, 15, 16),
    (17, 18, 19),
    (20, 21, 22),
    (0, 8, 20),
    (3, 9, 17),
    (6, 10, 14),
    (15, 18, 21),
    (7, 11, 16),
    (5, 12, 19),
    (2, 13, 22),
    (0, 3, 6),
    (2, 5, 7),
    (14, 17, 20),
    (16, 19, 22),
)


def close_mill(index: int, board: str) -> bool:
    """Return whether the piece at ``index`` belongs to a completed mill."""
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError("Board index must be an integer.")
    if not 0 <= index < 23:
        raise IndexError("Board index must be between 0 and 22.")
    if not is_valid_board(board):
        raise ValueError("Board must be a valid 23-character board string.")

    symbol = board[index]
    if symbol == EMPTY:
        return False

    return any(
        index in mill
        and all(board[position] == symbol for position in mill)
        for mill in MILL_LINES
    )
