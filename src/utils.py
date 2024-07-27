from typing import Tuple

BoardSquare = Tuple[int, int]
Movement = Tuple[BoardSquare, BoardSquare]

# A play can be either the movement of a piece, or the positioning of one (for the first goat moves).
Play = Movement | BoardSquare
