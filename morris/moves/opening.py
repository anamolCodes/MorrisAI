"""White opening move generation."""

from morris.board.constants import EMPTY, WHITE
from morris.board.representation import is_valid_board
from morris.rules.mills import close_mill
from morris.rules.removal import generate_remove


def generate_add(board: str) -> list[str]:
    """Generate White opening positions by placing a piece on an empty location."""
    if not is_valid_board(board):
        raise ValueError("Board must be a valid 23-character board string.")

    positions = []
    for index, piece in enumerate(board):
        if piece != EMPTY:
            continue

        updated_board = list(board)
        updated_board[index] = WHITE
        updated_board = "".join(updated_board)

        if close_mill(index, updated_board):
            positions.extend(generate_remove(updated_board))
        else:
            positions.append(updated_board)

    return positions
