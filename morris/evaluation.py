"""Original and improved static evaluation functions for MorrisAI.

All evaluation functions score a board from White's point of view:
positive scores favor White and negative scores favor Black.
"""

from morris.board.constants import BLACK, EMPTY, WHITE
from morris.board.representation import is_valid_board
from morris.moves.black import generate_black_midgame_endgame, generate_black_opening
from morris.moves.midgame_endgame import generate_midgame_endgame
from morris.moves.opening import generate_add
from morris.rules.mills import MILL_LINES

WIN_SCORE = 10_000


def _validate(board: str) -> None:
    if not is_valid_board(board):
        raise ValueError("Board must be a valid 23-character board string.")


def _count_mills(board: str, color: str) -> int:
    """Count completed mill lines belonging to the given color."""
    return sum(all(board[index] == color for index in line) for line in MILL_LINES)


def _count_potential_mills(board: str, color: str) -> int:
    """Count mill lines with two pieces of color and one empty location."""
    count = 0
    for line in MILL_LINES:
        values = [board[index] for index in line]
        if values.count(color) == 2 and values.count(EMPTY) == 1:
            count += 1
    return count


def static_estimation_opening(board: str) -> int:
    """Return the assignment's original opening evaluation (White minus Black pieces)."""
    _validate(board)
    return board.count(WHITE) - board.count(BLACK)


def static_estimation_midgame_endgame(board: str) -> int:
    """Return the assignment's original midgame/endgame evaluation."""
    _validate(board)
    white_pieces = board.count(WHITE)
    black_pieces = board.count(BLACK)

    if black_pieces <= 2:
        return WIN_SCORE
    if white_pieces <= 2:
        return -WIN_SCORE

    black_moves = len(generate_black_midgame_endgame(board))
    if black_moves == 0:
        return WIN_SCORE

    return 1000 * (white_pieces - black_pieces) - black_moves


def improved_static_estimation_opening(board: str) -> int:
    
    _validate(board)
    white_pieces = board.count(WHITE)
    black_pieces = board.count(BLACK)

    piece_difference = white_pieces - black_pieces
    mill_difference = _count_mills(board, WHITE) - _count_mills(board, BLACK)
    potential_difference = (
        _count_potential_mills(board, WHITE)
        - _count_potential_mills(board, BLACK)
    )

    return (
        1000 * piece_difference
        + 40 * mill_difference
        + 20 * potential_difference
    )


def improved_static_estimation_midgame_endgame(board: str) -> int:
    """Score a game-phase board using material, mills, threats, and mobility. """

    _validate(board)
    white_pieces = board.count(WHITE)
    black_pieces = board.count(BLACK)

    if black_pieces <= 2:
        return WIN_SCORE
    if white_pieces <= 2:
        return -WIN_SCORE

    black_moves = len(generate_black_midgame_endgame(board))
    if black_moves == 0:
        return WIN_SCORE

    white_moves = len(generate_midgame_endgame(board))
    if white_moves == 0:
        return -WIN_SCORE

    piece_difference = white_pieces - black_pieces
    mill_difference = _count_mills(board, WHITE) - _count_mills(board, BLACK)
    potential_difference = (
        _count_potential_mills(board, WHITE)
        - _count_potential_mills(board, BLACK)
    )
    mobility_difference = white_moves - black_moves

    return (
        1000 * piece_difference
        + 40 * mill_difference
        + 20 * potential_difference
        + 2 * mobility_difference
    )


def get_legal_move_count(board: str, color: str, phase: str) -> int:
    """Return the generated successor-position count for a color and phase."""
    
    _validate(board)
    if color == WHITE and phase == "opening":
        return len(generate_add(board))
    if color == BLACK and phase == "opening":
        return len(generate_black_opening(board))
    if color == WHITE and phase == "game":
        return len(generate_midgame_endgame(board))
    if color == BLACK and phase == "game":
        return len(generate_black_midgame_endgame(board))
    if color not in (WHITE, BLACK):
        raise ValueError("color must be 'W' or 'B'.")
    raise ValueError("phase must be 'opening' or 'game'.")
