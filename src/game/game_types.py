from dataclasses import dataclass


@dataclass(frozen=True)
class BoardSquare:
    """A position in the board"""

    lin: int
    col: int


@dataclass
class Movement:
    """Defines a movement in the board"""

    start: BoardSquare
    end: BoardSquare


@dataclass
class Capture:
    """Defines a capture of a piece"""

    starting_square: BoardSquare
    captured: BoardSquare
    ending_square: BoardSquare


# A play can be either the movement of a piece, or the positioning of one (for the first goat moves).
Play = Capture | Movement | BoardSquare
