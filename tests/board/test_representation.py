"""Tests for board representation."""

import pytest

from morris.board.representation import is_valid_board


def test_empty_board_is_valid():
    assert is_valid_board("x" * 23) is True


def test_mixed_board_is_valid():
    assert is_valid_board("W" + ("x" * 10) + "B" + ("x" * 11)) is True


@pytest.mark.parametrize(
    "board",
    (
        "x" * 22,
        "x" * 24,
        ("x" * 22) + "?",
        ("x" * 22) + "w",
        ("x" * 22) + "b",
        "",
        None,
        23,
        [],
        (),
    ),
)
def test_invalid_board_values_are_rejected(board):
    assert is_valid_board(board) is False
