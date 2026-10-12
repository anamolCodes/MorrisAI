
"""Tests for original and improved evaluation functions."""

import pytest

from morris.board.constants import BLACK, EMPTY, WHITE
from morris.evaluation import (
    improved_static_estimation_midgame_endgame,
    improved_static_estimation_opening,
    static_estimation_midgame_endgame,
    static_estimation_opening,
)


def board_with(pieces: dict[int, str]) -> str:
    board = [EMPTY] * 23
    for index, piece in pieces.items():
        board[index] = piece
    return "".join(board)


def test_original_opening_counts_piece_difference():
    board = board_with({
        0: WHITE,
        1: WHITE,
        10: WHITE,
        14: BLACK,
    })
    assert static_estimation_opening(board) == 2


def test_original_opening_equal_pieces_returns_zero():
    board = board_with({
        0: WHITE,
        1: WHITE,
        10: BLACK,
        14: BLACK,
    })
    assert static_estimation_opening(board) == 0


def test_improved_opening_rewards_potential_mill():
    # White at 0 and 1 can complete the mill (0, 1, 2).
    board = board_with({
        0: WHITE,
        1: WHITE,
        10: BLACK,
    })
    assert improved_static_estimation_opening(board) == 1020


def test_original_game_detects_white_win():
    board = board_with({
        0: WHITE,
        4: WHITE,
        8: WHITE,
        10: BLACK,
        21: BLACK,
    })
    assert static_estimation_midgame_endgame(board) == 10000


def test_original_game_detects_white_loss():
    board = board_with({
        0: WHITE,
        4: WHITE,
        8: BLACK,
        10: BLACK,
        14: BLACK,
    })
    assert static_estimation_midgame_endgame(board) == -10000


def test_improved_game_detects_white_win():
    board = board_with({
        0: WHITE,
        4: WHITE,
        8: WHITE,
        10: BLACK,
        21: BLACK,
    })
    assert improved_static_estimation_midgame_endgame(board) == 10000


@pytest.mark.parametrize(
    "invalid_board",
    ("x" * 22, "x" * 24, None, 23),
)
def test_evaluation_rejects_invalid_boards(invalid_board):
    with pytest.raises(ValueError):
        static_estimation_opening(invalid_board)

    with pytest.raises(ValueError):
        improved_static_estimation_opening(invalid_board)
