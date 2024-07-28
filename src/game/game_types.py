from dataclasses import dataclass


@dataclass(frozen=True)
class BoardSquare:
    """A position in the board"""

    lin: int
    col: int

    def __str__(self) -> str:
        return f"({self.lin}, {self.col})"


@dataclass
class Movement:
    """Defines a movement in the board"""

    start: BoardSquare
    end: BoardSquare

    def __str__(self) -> str:
        return f"({self.start.lin}, {self.start.col} -> ({self.end.lin}, {self.end.col})"


@dataclass
class Capture:
    """Defines a capture of a piece"""

    starting_square: BoardSquare
    captured: BoardSquare
    ending_square: BoardSquare

    def __str__(self) -> str:
        return (
            f"({self.starting_square.lin}, {self.starting_square.col})"
            f" Capturing ({self.captured.lin}, {self.captured.col})"
            f" -> ({self.ending_square.lin}, {self.ending_square.col})"
        )


# A play can be either the movement of a piece, or the positioning of one (for the first goat moves).
Play = Capture | Movement | BoardSquare
