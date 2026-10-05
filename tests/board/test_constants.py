"""Tests for board constants."""

from morris.board.constants import (
    BLACK,
    BOARD_SIZE,
    EMPTY,
    VALID_SYMBOLS,
    WHITE,
)


def test_board_size_is_23():
    assert BOARD_SIZE == 23


def test_white_symbol_is_W():
    assert WHITE == "W"


def test_black_symbol_is_B():
    assert BLACK == "B"


def test_empty_symbol_is_x():
    assert EMPTY == "x"


def test_valid_symbols_contain_exactly_the_board_symbols():
    assert VALID_SYMBOLS == {"W", "B", "x"}


def test_no_additional_board_symbols_are_valid():
    assert "w" not in VALID_SYMBOLS
    assert "b" not in VALID_SYMBOLS
    assert " " not in VALID_SYMBOLS
    assert "." not in VALID_SYMBOLS
    assert "@" not in VALID_SYMBOLS
