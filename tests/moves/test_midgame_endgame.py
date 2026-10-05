"""Tests for White midgame/endgame move-generation selection."""

import pytest

from morris.board.constants import BLACK, EMPTY, WHITE
from morris.moves.midgame_endgame import generate_midgame_endgame


def board_with(pieces: dict[int, str]) -> str:
    board = [EMPTY] * 23
    for index, piece in pieces.items():
        board[index] = piece
    return "".join(board)


def moved_board(board: str, source: int, destination: int) -> str:
    updated_board = list(board)
    updated_board[source] = EMPTY
    updated_board[destination] = WHITE
    return "".join(updated_board)


def test_exactly_three_white_pieces_uses_hopping():
    board = board_with({0: WHITE, 10: WHITE, 15: WHITE})

    assert moved_board(board, 0, 22) in generate_midgame_endgame(board)


def test_more_than_three_white_pieces_uses_adjacent_movement():
    board = board_with({0: WHITE, 10: WHITE, 15: WHITE, 21: WHITE})
    results = generate_midgame_endgame(board)

    assert moved_board(board, 0, 1) in results
    assert moved_board(board, 0, 22) not in results


def test_exactly_four_white_pieces_does_not_use_hopping():
    board = board_with({0: WHITE, 10: WHITE, 15: WHITE, 21: WHITE})

    assert moved_board(board, 0, 22) not in generate_midgame_endgame(board)


def test_three_white_pieces_can_still_move_to_an_adjacent_location():
    board = board_with({0: WHITE, 10: WHITE, 15: WHITE})

    assert moved_board(board, 0, 1) in generate_midgame_endgame(board)


def test_three_piece_hopping_mill_triggers_removal():
    board = board_with({0: WHITE, 1: WHITE, 22: WHITE, 7: BLACK})
    placed = moved_board(board, 22, 2)
    expected = placed[:7] + EMPTY + placed[8:]

    assert expected in generate_midgame_endgame(board)


def test_normal_movement_mill_triggers_removal_with_more_than_three_white_pieces():
    board = board_with({0: WHITE, 9: WHITE, 20: WHITE, 21: WHITE, 4: BLACK})
    placed = moved_board(board, 9, 8)
    expected = placed[:4] + EMPTY + placed[5:]

    assert expected in generate_midgame_endgame(board)


def test_original_board_remains_unchanged():
    board = board_with({0: WHITE, 10: WHITE, 15: WHITE})

    generate_midgame_endgame(board)

    assert board == board_with({0: WHITE, 10: WHITE, 15: WHITE})


@pytest.mark.parametrize("invalid_board", (EMPTY * 22, EMPTY * 24, None, 23))
def test_invalid_boards_raise_value_error(invalid_board):
    with pytest.raises(ValueError):
        generate_midgame_endgame(invalid_board)
