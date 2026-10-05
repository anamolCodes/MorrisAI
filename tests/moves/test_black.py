"""Tests for Black move generation through color swapping."""

import pytest

from morris.board.constants import BLACK, EMPTY, WHITE
from morris.moves.black import (
    generate_black_midgame_endgame,
    generate_black_opening,
    swap_colors,
)


def board_with(pieces: dict[int, str]) -> str:
    board = [EMPTY] * 23
    for index, piece in pieces.items():
        board[index] = piece
    return "".join(board)


def moved_board(board: str, source: int, destination: int, piece: str) -> str:
    updated_board = list(board)
    updated_board[source] = EMPTY
    updated_board[destination] = piece
    return "".join(updated_board)


def test_swap_colors_changes_white_to_black():
    assert swap_colors("W" + EMPTY * 22) == "B" + EMPTY * 22


def test_swap_colors_changes_black_to_white():
    assert swap_colors("B" + EMPTY * 22) == "W" + EMPTY * 22


def test_swap_colors_leaves_empty_unchanged():
    assert swap_colors(EMPTY * 23) == EMPTY * 23


def test_swapping_twice_returns_original_board():
    board = board_with({0: WHITE, 1: BLACK, 22: WHITE})

    assert swap_colors(swap_colors(board)) == board


@pytest.mark.parametrize("invalid_board", (EMPTY * 22, EMPTY * 24, None, 23))
def test_invalid_boards_raise_value_error_in_swap_colors(invalid_board):
    with pytest.raises(ValueError):
        swap_colors(invalid_board)


def test_black_opening_can_add_black_to_empty_position():
    board = EMPTY * 23
    expected = board[:0] + BLACK + board[1:]

    assert expected in generate_black_opening(board)


def test_black_opening_does_not_overwrite_existing_pieces():
    board = board_with({0: WHITE, 1: BLACK})
    results = generate_black_opening(board)

    assert all(result[0] == WHITE for result in results)
    assert all(result[1] == BLACK for result in results)


def test_black_opening_mill_removes_eligible_white_piece():
    board = board_with({0: BLACK, 1: BLACK, 7: WHITE})
    placed = board[:2] + BLACK + board[3:]
    expected = placed[:7] + EMPTY + placed[8:]

    assert expected in generate_black_opening(board)


def test_black_opening_mill_generates_all_eligible_white_removals():
    board = board_with({0: BLACK, 1: BLACK, 7: WHITE, 10: WHITE})
    placed = board[:2] + BLACK + board[3:]
    expected = {
        placed[:7] + EMPTY + placed[8:],
        placed[:10] + EMPTY + placed[11:],
    }

    assert expected.issubset(generate_black_opening(board))


def test_black_midgame_uses_adjacent_movement_with_more_than_three_black_pieces():
    board = board_with({0: BLACK, 10: BLACK, 15: BLACK, 21: BLACK})
    results = generate_black_midgame_endgame(board)

    assert moved_board(board, 0, 1, BLACK) in results


def test_black_midgame_does_not_use_distant_hopping_with_more_than_three_black():
    board = board_with({0: BLACK, 10: BLACK, 15: BLACK, 21: BLACK})

    assert moved_board(board, 0, 22, BLACK) not in generate_black_midgame_endgame(board)


def test_black_endgame_with_three_black_pieces_allows_distant_hopping():
    board = board_with({0: BLACK, 10: BLACK, 15: BLACK})

    assert moved_board(board, 0, 22, BLACK) in generate_black_midgame_endgame(board)


def test_black_hopping_mill_removes_eligible_white_piece():
    board = board_with({0: BLACK, 1: BLACK, 22: BLACK, 7: WHITE})
    placed = moved_board(board, 22, 2, BLACK)
    expected = placed[:7] + EMPTY + placed[8:]

    assert expected in generate_black_midgame_endgame(board)


def test_white_pieces_are_not_accidentally_moved():
    board = board_with({0: BLACK, 10: WHITE})
    results = generate_black_midgame_endgame(board)

    assert all(result[10] == WHITE for result in results)


def test_ordinary_black_movement_preserves_black_piece_count():
    board = board_with({0: BLACK, 10: BLACK, 15: BLACK, 21: BLACK})

    assert all(
        result.count(BLACK) == board.count(BLACK)
        for result in generate_black_midgame_endgame(board)
    )


def test_black_move_generation_does_not_mutate_original_board():
    board = board_with({0: BLACK, 10: BLACK, 15: BLACK})

    generate_black_midgame_endgame(board)

    assert board == board_with({0: BLACK, 10: BLACK, 15: BLACK})


@pytest.mark.parametrize("invalid_board", (EMPTY * 22, EMPTY * 24, None, 23))
def test_invalid_boards_raise_value_error_in_black_generators(invalid_board):
    with pytest.raises(ValueError):
        generate_black_opening(invalid_board)
    with pytest.raises(ValueError):
        generate_black_midgame_endgame(invalid_board)
