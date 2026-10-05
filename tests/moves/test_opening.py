"""Tests for White opening move generation."""

import pytest

from morris.board.constants import BLACK, EMPTY, WHITE
from morris.moves.opening import generate_add


def board_with(pieces: dict[int, str]) -> str:
    board = [EMPTY] * 23
    for index, piece in pieces.items():
        board[index] = piece
    return "".join(board)


def board_after_placement(board: str, index: int) -> str:
    updated_board = list(board)
    updated_board[index] = WHITE
    return "".join(updated_board)


def test_empty_board_generates_23_opening_positions():
    results = generate_add(EMPTY * 23)

    assert len(results) == 23


def test_empty_board_results_have_one_white_piece_and_no_black_pieces():
    results = generate_add(EMPTY * 23)

    assert all(result.count(WHITE) == 1 for result in results)
    assert all(result.count(BLACK) == 0 for result in results)
    assert all(result.count(EMPTY) == 22 for result in results)


def test_empty_board_results_place_white_at_every_index():
    board = EMPTY * 23

    assert generate_add(board) == [
        board_after_placement(board, index) for index in range(23)
    ]


def test_occupied_locations_are_not_used_for_placement():
    board = board_with({0: WHITE})

    results = generate_add(board)

    assert len(results) == 22
    assert all(result[0] == WHITE for result in results)
    assert all(result.count(WHITE) == 2 for result in results)


def test_black_occupied_locations_are_not_used_for_placement():
    board = board_with({0: BLACK})

    results = generate_add(board)

    assert len(results) == 22
    assert all(result[0] == BLACK for result in results)


def test_normal_placement_produces_expected_board():
    board = board_with({0: WHITE})
    expected = board_after_placement(board, 4)

    assert expected in generate_add(board)


def test_mill_placement_triggers_black_piece_removal():
    board = board_with({0: WHITE, 1: WHITE, 7: BLACK})
    placed = board_after_placement(board, 2)
    expected = placed[:7] + EMPTY + placed[8:]

    assert expected in generate_add(board)


def test_mill_placement_generates_one_result_per_eligible_black_piece():
    board = board_with({0: WHITE, 1: WHITE, 7: BLACK, 10: BLACK})
    placed = board_after_placement(board, 2)
    expected = {
        placed[:7] + EMPTY + placed[8:],
        placed[:10] + EMPTY + placed[11:],
    }

    results = generate_add(board)

    assert expected.issubset(results)


def test_protected_black_piece_is_not_removed_when_another_is_eligible():
    board = board_with(
        {0: WHITE, 1: WHITE, 3: BLACK, 4: BLACK, 5: BLACK, 7: BLACK}
    )
    placed = board_after_placement(board, 2)
    expected = placed[:7] + EMPTY + placed[8:]

    results = generate_add(board)

    assert expected in results
    assert placed[:3] + EMPTY + placed[4:] not in results


def test_original_board_remains_unchanged():
    board = board_with({0: WHITE, 1: WHITE, 7: BLACK})

    generate_add(board)

    assert board == board_with({0: WHITE, 1: WHITE, 7: BLACK})


def test_no_mill_placements_equal_number_of_empty_locations():
    board = board_with({0: WHITE})

    assert len(generate_add(board)) == board.count(EMPTY)


@pytest.mark.parametrize("invalid_board", (EMPTY * 22, EMPTY * 24, None, 23))
def test_invalid_boards_raise_value_error(invalid_board):
    with pytest.raises(ValueError):
        generate_add(invalid_board)
