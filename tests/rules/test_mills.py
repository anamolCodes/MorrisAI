"""Tests for Morris mill detection."""

import pytest

from morris.rules.mills import MILL_LINES, close_mill


EXPECTED_MILL_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (8, 9, 10),
    (11, 12, 13),
    (14, 15, 16),
    (17, 18, 19),
    (20, 21, 22),
    (0, 8, 20),
    (3, 9, 17),
    (6, 10, 14),
    (15, 18, 21),
    (7, 11, 16),
    (5, 12, 19),
    (2, 13, 22),
    (0, 3, 6),
    (2, 5, 7),
    (14, 17, 20),
    (16, 19, 22),
)


def board_with(symbol: str, positions: tuple[int, ...]) -> str:
    board = ["x"] * 23
    for position in positions:
        board[position] = symbol
    return "".join(board)


def test_mill_lines_contains_exactly_18_definitions():
    assert len(MILL_LINES) == 18


def test_mill_lines_match_authoritative_table():
    assert MILL_LINES == EXPECTED_MILL_LINES


def test_every_mill_has_three_distinct_locations():
    assert all(len(mill) == 3 and len(set(mill)) == 3 for mill in MILL_LINES)


def test_every_mill_index_is_valid():
    assert all(
        0 <= position <= 22
        for mill in MILL_LINES
        for position in mill
    )


def test_mill_lines_have_no_duplicates():
    assert len(MILL_LINES) == len(set(MILL_LINES))


@pytest.mark.parametrize("index", (0, 1, 2))
def test_completed_white_horizontal_mill_is_detected(index):
    board = board_with("W", (0, 1, 2))

    assert close_mill(index, board) is True


def test_completed_black_mill_is_detected():
    board = board_with("B", (17, 18, 19))

    assert close_mill(18, board) is True


def test_completed_vertical_mill_is_detected():
    board = board_with("W", (0, 8, 20))

    assert close_mill(8, board) is True


def test_completed_diagonal_mill_is_detected():
    board = board_with("B", (0, 3, 6))

    assert close_mill(3, board) is True


def test_incomplete_mill_is_not_detected():
    board = board_with("W", (0, 1))

    assert close_mill(0, board) is False


def test_mixed_colors_do_not_form_a_mill():
    board = list(board_with("W", (0, 1)))
    board[2] = "B"
    board = "".join(board)

    assert close_mill(0, board) is False


def test_empty_location_is_not_in_a_mill():
    board = board_with("W", (0, 1))

    assert close_mill(2, board) is False


def test_piece_can_complete_any_of_multiple_mill_lines():
    board = board_with("W", (0, 3, 6))

    assert close_mill(0, board) is True


def test_invalid_adjacent_combination_is_not_a_mill():
    board = board_with("W", (6, 7, 11))

    assert close_mill(7, board) is False


@pytest.mark.parametrize("invalid_index", (-1, 23, 100))
def test_out_of_range_indices_raise_index_error(invalid_index):
    with pytest.raises(IndexError):
        close_mill(invalid_index, "x" * 23)


@pytest.mark.parametrize("invalid_index", ("0", 0.0, None, True, False))
def test_non_integer_indices_raise_type_error(invalid_index):
    with pytest.raises(TypeError):
        close_mill(invalid_index, "x" * 23)


@pytest.mark.parametrize("invalid_board", ("x" * 22, "x" * 24, None, 23))
def test_invalid_boards_raise_value_error(invalid_board):
    with pytest.raises(ValueError):
        close_mill(0, invalid_board)
