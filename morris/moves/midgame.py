"""White midgame move generation."""

from morris.board.constants import EMPTY, WHITE
from morris.board.representation import is_valid_board
from morris.rules.mills import close_mill
from morris.rules.neighbors import neighbors
from morris.rules.removal import generate_remove


def generate_move(board: str) -> list[str]:
    """Generate White moves to adjacent empty board locations."""
    if not is_valid_board(board):
        raise ValueError("Board must be a valid 23-character board string.")

    positions = []
    for source, piece in enumerate(board):
        if piece != WHITE:
            continue

        for destination in neighbors(source):
            if board[destination] != EMPTY:
                continue

            updated_board = list(board)
            updated_board[source] = EMPTY
            updated_board[destination] = WHITE
            updated_board = "".join(updated_board)

            if close_mill(destination, updated_board):
                positions.extend(generate_remove(updated_board))
            else:
                positions.append(updated_board)

    return positions
