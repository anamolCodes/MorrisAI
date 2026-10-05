"""White midgame/endgame move-generation selection."""

from morris.board.constants import WHITE
from morris.board.representation import is_valid_board
from morris.moves.hopping import generate_hopping
from morris.moves.midgame import generate_move


def generate_midgame_endgame(board: str) -> list[str]:
    """Select hopping or adjacent movement based on White's piece count."""
    if not is_valid_board(board):
        raise ValueError("Board must be a valid 23-character board string.")

    if board.count(WHITE) == 3:
        return generate_hopping(board)
    return generate_move(board)
