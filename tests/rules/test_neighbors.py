"""Tests for Morris board adjacency relationships."""

import pytest

from morris.rules.neighbors import NEIGHBORS, neighbors


EXPECTED_NEIGHBORS = (
    (1, 3, 8),
    (0, 2, 4),
    (1, 5, 13),
    (0, 4, 6, 9),
    (1, 3, 5),
    (2, 4, 7, 12),
    (3, 7, 10),
    (5, 6, 11),
    (0, 9, 20),
    (3, 8, 10, 17),
    (6, 9, 14),
    (7, 12, 16),
    (5, 11, 13, 19),
    (2, 12, 22),
    (10, 15, 17),
    (14, 16, 18),
    (11, 15, 19),
    (9, 14, 18, 20),
    (15, 17, 19, 21),
    (12, 16, 18, 22),
    (8, 17, 21),
    (18, 20, 22),
    (13, 19, 21),
)


def test_there_are_23_adjacency_definitions():
    assert len(NEIGHBORS) == 23


@pytest.mark.parametrize(
    ("index", "expected"),
    (
        (0, (1, 3, 8)),
        (3, (0, 4, 6, 9)),
        (9, (3, 8, 10, 17)),
        (12, (5, 11, 13, 19)),
        (18, (15, 17, 19, 21)),
        (22, (13, 19, 21)),
    ),
)
def test_representative_neighbors(index, expected):
    assert neighbors(index) == expected


def test_entire_adjacency_table_matches_specification():
    assert NEIGHBORS == EXPECTED_NEIGHBORS


def test_every_neighbor_index_is_valid():
    for adjacent_locations in NEIGHBORS:
        assert all(0 <= adjacent_index <= 22 for adjacent_index in adjacent_locations)


def test_no_location_is_its_own_neighbor():
    for index, adjacent_locations in enumerate(NEIGHBORS):
        assert index not in adjacent_locations


def test_no_neighbor_list_contains_duplicates():
    for adjacent_locations in NEIGHBORS:
        assert len(adjacent_locations) == len(set(adjacent_locations))


def test_adjacency_is_symmetric():
    for index, adjacent_locations in enumerate(NEIGHBORS):
        for adjacent_index in adjacent_locations:
            assert index in neighbors(adjacent_index)


@pytest.mark.parametrize(
    "invalid_index",
    (-1, 23, 100, "0", 0.0, None, True, False),
)
def test_invalid_indices_are_rejected(invalid_index):
    with pytest.raises((IndexError, TypeError)):
        neighbors(invalid_index)
