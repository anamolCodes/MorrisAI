"""Tests for Morris piece removal."""

import pytest

from morris.board.constants import BLACK, EMPTY, WHITE
from morris.rules.removal import generate_remove


def board_with(pieces: dict[int, str]) -> str:
    board = [EMPTY] * 23
    for index, piece in pieces.items():
        board[index] = piece
    return "".join(board)


def test_single_isolated_black_piece_can_be_removed():
    board = board_with({4: BLACK})

    assert generate_remove(board) == [board[:4] + EMPTY + board[5:]]


def test_multiple_isolated_black_pieces_generate_one_board_each():
    board = board_with({4: BLACK, 7: BLACK})

    assert generate_remove(board) == [
        board[:4] + EMPTY + board[5:],
        board[:7] + EMPTY + board[8:],
    ]


def test_black_piece_in_mill_is_not_removed_when_another_is_eligible():
    board = board_with({0: BLACK, 1: BLACK, 2: BLACK, 4: BLACK})

    results = generate_remove(board)

    assert results == [board[:4] + EMPTY + board[5:]]


def test_only_black_piece_outside_mill_may_be_removed():
    board = board_with({0: BLACK, 1: BLACK, 2: BLACK, 4: BLACK})

    results = generate_remove(board)

    assert len(results) == 1
    assert results[0][4] == EMPTY
    assert all(results[0][index] == BLACK for index in (0, 1, 2))


def test_all_black_pieces_in_mills_use_fallback():
    board = board_with({0: BLACK, 1: BLACK, 2: BLACK})

    assert generate_remove(board) == [board]


def test_no_black_pieces_use_fallback():
    board = board_with({0: WHITE, 4: WHITE})

    assert generate_remove(board) == [board]


def test_white_pieces_are_never_removed():
    board = board_with({0: WHITE, 4: BLACK})

    result = generate_remove(board)[0]

    assert result[0] == WHITE
    assert result[4] == EMPTY


def test_original_board_remains_unchanged():
    board = board_with({4: BLACK})

    generate_remove(board)

    assert board == board_with({4: BLACK})


def test_each_generated_board_changes_one_eligible_black_piece_to_empty():
    board = board_with({4: BLACK, 7: BLACK})

    for result in generate_remove(board):
        differences = [
            index
            for index, (original, updated) in enumerate(zip(board, result))
            if original != updated
        ]
        assert len(differences) == 1
        changed_index = differences[0]
        assert board[changed_index] == BLACK
        assert result[changed_index] == EMPTY


@pytest.mark.parametrize("invalid_board", ("x" * 22, "x" * 24, None, 23))
def test_invalid_boards_raise_value_error(invalid_board):
    with pytest.raises(ValueError):
        generate_remove(invalid_board)
