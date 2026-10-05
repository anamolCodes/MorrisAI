"""White move-generation piece removal after forming a mill."""

from morris.board.constants import BLACK, EMPTY
from morris.board.representation import is_valid_board
from morris.rules.mills import close_mill


def generate_remove(board: str) -> list[str]:
    """Generate boards formed by removing eligible black pieces."""
    if not is_valid_board(board):
        raise ValueError("Board must be a valid 23-character board string.")

    positions = []
    for index, piece in enumerate(board):
        if piece == BLACK and not close_mill(index, board):
            updated_board = list(board)
            updated_board[index] = EMPTY
            positions.append("".join(updated_board))

    return positions or [board]
