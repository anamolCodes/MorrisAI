"""Tests for board coordinate mapping."""

import pytest

from morris.board.mapping import (
    COORDINATE_TO_INDEX,
    INDEX_TO_COORDINATE,
    coordinate_for_index,
    index_for_coordinate,
)


EXPECTED_COORDINATES = (
    "a0",
    "d0",
    "g0",
    "b1",
    "d1",
    "f1",
    "c2",
    "e2",
    "a3",
    "b3",
    "c3",
    "e3",
    "f3",
    "g3",
    "c4",
    "d4",
    "e4",
    "b5",
    "d5",
    "f5",
    "a6",
    "d6",
    "g6",
)


def test_mapping_contains_exactly_23_locations():
    assert len(INDEX_TO_COORDINATE) == 23
    assert len(COORDINATE_TO_INDEX) == 23


def test_index_to_coordinate_order_matches_specification():
    assert INDEX_TO_COORDINATE == EXPECTED_COORDINATES


def test_representative_index_to_coordinate_lookups():
    assert coordinate_for_index(0) == "a0"
    assert coordinate_for_index(10) == "c3"
    assert coordinate_for_index(22) == "g6"

def test_representative_coordinate_to_index_lookups():
    assert index_for_coordinate("a0") == 0
    assert index_for_coordinate("c3") == 10
    assert index_for_coordinate("g6") == 22


def test_every_coordinate_is_unique():
    assert len(set(INDEX_TO_COORDINATE)) == 23


def test_every_mapping_round_trip_returns_original_index():
    for index, coordinate in enumerate(INDEX_TO_COORDINATE):
        assert index_for_coordinate(coordinate_for_index(index)) == index

