"""Black move generation through color-swapped White generators."""

from morris.board.constants import BLACK, WHITE
from morris.board.representation import is_valid_board
from morris.moves.midgame_endgame import generate_midgame_endgame
from morris.moves.opening import generate_add


def swap_colors(board: str) -> str:
    """Swap White and Black pieces while leaving empty locations unchanged."""
    if not is_valid_board(board):
        raise ValueError("Board must be a valid 23-character board string.")

    swapped = {WHITE: BLACK, BLACK: WHITE}
    return "".join(swapped.get(piece, piece) for piece in board)


def generate_black_opening(board: str) -> list[str]:
    """Generate Black opening positions through color-swapped White generation."""
    swapped_results = generate_add(swap_colors(board))
    return [swap_colors(result) for result in swapped_results]


def generate_black_midgame_endgame(board: str) -> list[str]:
    """Generate Black midgame/endgame positions through color swapping."""
    swapped_results = generate_midgame_endgame(swap_colors(board))
    return [swap_colors(result) for result in swapped_results]
