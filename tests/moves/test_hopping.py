"""Tests for White hopping move generation."""

import pytest

from morris.board.constants import BLACK, EMPTY, WHITE
from morris.moves.hopping import generate_hopping


def board_with(pieces: dict[int, str]) -> str:
    board = [EMPTY] * 23
    for index, piece in pieces.items():
        board[index] = piece
    return "".join(board)


def hopped_board(board: str, source: int, destination: int) -> str:
    updated_board = list(board)
    updated_board[source] = EMPTY
    updated_board[destination] = WHITE
    return "".join(updated_board)


def test_white_piece_can_hop_to_distant_empty_non_neighbor():
    board = board_with({0: WHITE})

    assert hopped_board(board, 0, 22) in generate_hopping(board)


def test_white_piece_can_hop_to_adjacent_empty_location():
    board = board_with({0: WHITE})

    assert hopped_board(board, 0, 1) in generate_hopping(board)


def test_white_piece_cannot_hop_onto_another_white_piece():
    board = board_with({0: WHITE, 22: WHITE})

    assert hopped_board(board, 0, 22) not in generate_hopping(board)


def test_white_piece_cannot_hop_onto_a_black_piece():
    board = board_with({0: WHITE, 22: BLACK})

    assert hopped_board(board, 0, 22) not in generate_hopping(board)


def test_hop_clears_source_and_places_white_at_destination():
    board = board_with({0: WHITE})
    result = hopped_board(board, 0, 22)

    assert result[0] == EMPTY
    assert result[22] == WHITE


def test_normal_hop_preserves_white_piece_count():
    board = board_with({0: WHITE, 10: WHITE})

    assert all(
        result.count(WHITE) == board.count(WHITE)
        for result in generate_hopping(board)
    )


def test_multiple_white_pieces_generate_hopping_possibilities():
    board = board_with({0: WHITE, 22: WHITE})

    results = generate_hopping(board)

    assert hopped_board(board, 0, 1) in results
    assert hopped_board(board, 22, 1) in results


def test_no_white_pieces_returns_no_moves():
    assert generate_hopping(board_with({0: BLACK})) == []


def test_no_empty_locations_returns_no_moves():
    assert generate_hopping(BLACK * 23) == []


def test_mill_forming_hop_triggers_black_piece_removal():
    board = board_with({0: WHITE, 1: WHITE, 22: WHITE, 7: BLACK})
    placed = hopped_board(board, 22, 2)
    expected = placed[:7] + EMPTY + placed[8:]

    assert expected in generate_hopping(board)


def test_mill_forming_hop_generates_one_result_per_eligible_removal():
    board = board_with({0: WHITE, 1: WHITE, 22: WHITE, 7: BLACK, 10: BLACK})
    placed = hopped_board(board, 22, 2)
    expected = {
        placed[:7] + EMPTY + placed[8:],
        placed[:10] + EMPTY + placed[11:],
    }

    assert expected.issubset(generate_hopping(board))


def test_protected_black_piece_is_not_removed_when_another_is_eligible():
    board = board_with(
        {0: WHITE, 1: WHITE, 22: WHITE, 3: BLACK, 4: BLACK, 5: BLACK, 7: BLACK}
    )
    placed = hopped_board(board, 22, 2)
    removable = placed[:7] + EMPTY + placed[8:]
    protected = placed[:3] + EMPTY + placed[4:]

    results = generate_hopping(board)

    assert removable in results
    assert protected not in results


def test_original_board_remains_unchanged():
    board = board_with({0: WHITE, 22: BLACK})

    generate_hopping(board)

    assert board == board_with({0: WHITE, 22: BLACK})


@pytest.mark.parametrize("invalid_board", (EMPTY * 22, EMPTY * 24, None, 23))
def test_invalid_boards_raise_value_error(invalid_board):
    with pytest.raises(ValueError):
        generate_hopping(invalid_board)
