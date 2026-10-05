"""Mapping between Morris board indices and coordinate labels."""

from types import MappingProxyType

from morris.board.constants import BOARD_SIZE


INDEX_TO_COORDINATE = (
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

if len(INDEX_TO_COORDINATE) != BOARD_SIZE:
    raise ValueError("The board coordinate mapping must contain 23 locations.")
if len(set(INDEX_TO_COORDINATE)) != BOARD_SIZE:
    raise ValueError("The board coordinate mapping must contain unique locations.")

COORDINATE_TO_INDEX = MappingProxyType(
    {coordinate: index for index, coordinate in enumerate(INDEX_TO_COORDINATE)}
)


def coordinate_for_index(index: int) -> str:
    """Return the coordinate label for a board index."""
    return INDEX_TO_COORDINATE[index]


def index_for_coordinate(coordinate: str) -> int:
    """Return the board index for a coordinate label."""
    return COORDINATE_TO_INDEX[coordinate]