"""Adjacency relationships for the Morris board."""

NEIGHBORS = (
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


def neighbors(index: int) -> tuple[int, ...]:
    """Return the board locations adjacent to ``index``."""
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError("Board index must be an integer.")
    if not 0 <= index < len(NEIGHBORS):
        raise IndexError("Board index must be between 0 and 22.")
    return NEIGHBORS[index]
