"""Tests for White midgame move generation."""

import pytest

from morris.board.constants import BLACK, EMPTY, WHITE
from morris.moves.midgame import generate_move


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


def test_white_piece_can_move_to_each_empty_neighbor():
    board = board_with({0: WHITE})

    results = generate_move(board)

    assert moved_board(board, 0, 1) in results
    assert moved_board(board, 0, 3) in results
    assert moved_board(board, 0, 8) in results


def test_white_piece_cannot_move_to_a_non_neighbor():
    board = board_with({0: WHITE})

    assert moved_board(board, 0, 22) not in generate_move(board)


def test_white_piece_cannot_move_onto_another_white_piece():
    board = board_with({0: WHITE, 1: WHITE})

    assert moved_board(board, 0, 1) not in generate_move(board)


def test_white_piece_cannot_move_onto_a_black_piece():
    board = board_with({0: WHITE, 1: BLACK})

    assert moved_board(board, 0, 1) not in generate_move(board)


def test_multiple_white_pieces_generate_moves_for_each_piece():
    board = board_with({0: WHITE, 22: WHITE})

    results = generate_move(board)

    assert moved_board(board, 0, 1) in results
    assert moved_board(board, 0, 3) in results
    assert moved_board(board, 0, 8) in results
    assert moved_board(board, 22, 13) in results
    assert moved_board(board, 22, 19) in results
    assert moved_board(board, 22, 21) in results


def test_blocked_white_piece_generates_no_moves():
    board = board_with({0: WHITE, 1: BLACK, 3: BLACK, 8: BLACK})

    assert generate_move(board) == []


def test_normal_move_produces_expected_board():
    board = board_with({0: WHITE})
    expected = moved_board(board, 0, 1)

    assert expected in generate_move(board)


def test_mill_forming_move_triggers_black_piece_removal():
    board = board_with({0: WHITE, 9: WHITE, 20: WHITE, 4: BLACK})
    placed = moved_board(board, 9, 8)
    expected = placed[:4] + EMPTY + placed[5:]

    assert expected in generate_move(board)


def test_mill_forming_move_generates_one_result_per_eligible_removal():
    board = board_with({0: WHITE, 9: WHITE, 20: WHITE, 4: BLACK, 7: BLACK})
    placed = moved_board(board, 9, 8)
    expected = {
        placed[:4] + EMPTY + placed[5:],
        placed[:7] + EMPTY + placed[8:],
    }

    assert expected.issubset(generate_move(board))


def test_protected_black_piece_is_not_removed_when_another_is_eligible():
    board = board_with(
        {0: WHITE, 9: WHITE, 20: WHITE, 3: BLACK, 4: BLACK, 5: BLACK, 7: BLACK}
    )
    placed = moved_board(board, 9, 8)
    removable = placed[:7] + EMPTY + placed[8:]
    protected = placed[:3] + EMPTY + placed[4:]

    results = generate_move(board)

    assert removable in results
    assert protected not in results


def test_move_clears_source_and_places_white_at_destination():
    board = board_with({0: WHITE})
    result = moved_board(board, 0, 1)

    assert result[0] == EMPTY
    assert result[1] == WHITE


def test_normal_move_preserves_white_piece_count():
    board = board_with({0: WHITE, 22: WHITE})

    assert all(result.count(WHITE) == board.count(WHITE) for result in generate_move(board))


def test_original_board_remains_unchanged():
    board = board_with({0: WHITE, 4: BLACK})

    generate_move(board)

    assert board == board_with({0: WHITE, 4: BLACK})


def test_no_white_pieces_returns_no_moves():
    assert generate_move(board_with({0: BLACK})) == []


def test_white_pieces_without_empty_adjacent_destinations_return_no_moves():
    board = board_with({0: WHITE, 1: BLACK, 3: BLACK, 8: BLACK})

    assert generate_move(board) == []


@pytest.mark.parametrize("invalid_board", (EMPTY * 22, EMPTY * 24, None, 23))
def test_invalid_boards_raise_value_error(invalid_board):
    with pytest.raises(ValueError):
        generate_move(invalid_board)
