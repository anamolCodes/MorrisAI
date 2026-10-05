"""Validation for the structural representation of a Morris board."""

from morris.board.constants import BOARD_SIZE, VALID_SYMBOLS


def is_valid_board(board: object) -> bool:
    """Return whether ``board`` is a valid 23-character Morris board string."""
    return (
        isinstance(board, str)
        and len(board) == BOARD_SIZE
        and set(board).issubset(VALID_SYMBOLS)
    )