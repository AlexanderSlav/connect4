from dataclasses import dataclass
from enum import Enum


class Player(Enum):
    """Player enumeration for type safety"""

    RED = "🔴"
    YELLOW = "🟡"
    EMPTY = "⚪"

    @property
    def symbol(self) -> str:
        """Get the symbol representation"""
        return self.value

    @property
    def name_str(self) -> str:
        """Get the string name"""
        return self.name.lower()

    def opposite(self) -> "Player":
        """Get the opposite player"""
        if self == Player.RED:
            return Player.YELLOW
        elif self == Player.YELLOW:
            return Player.RED
        else:
            return Player.EMPTY


class GameState(Enum):
    """Game state enumeration"""

    PLAYING = "playing"
    RED_WINS = "red_wins"
    YELLOW_WINS = "yellow_wins"
    DRAW = "draw"

    @property
    def is_game_over(self) -> bool:
        """Check if the game is over"""
        return self != GameState.PLAYING


class Direction(Enum):
    """Direction enumeration for win checking"""

    HORIZONTAL = (0, 1)
    VERTICAL = (1, 0)
    DIAGONAL_RIGHT = (1, 1)
    DIAGONAL_LEFT = (1, -1)

    @property
    def delta_row(self) -> int:
        """Get row delta for this direction"""
        return self.value[0]

    @property
    def delta_col(self) -> int:
        """Get column delta for this direction"""
        return self.value[1]


class MoveResult(Enum):
    """Move result enumeration"""

    SUCCESS = "success"
    INVALID_COLUMN = "invalid_column"
    COLUMN_FULL = "column_full"
    GAME_OVER = "game_over"


@dataclass(frozen=True)
class Position:
    """Represents a position on the board"""

    row: int
    col: int

    def is_valid(self, max_rows: int, max_cols: int) -> bool:
        """Check if position is valid for given board dimensions"""
        return 0 <= self.row < max_rows and 0 <= self.col < max_cols

    def move_by(self, delta_row: int, delta_col: int) -> "Position":
        """Create a new position moved by the given deltas"""
        return Position(self.row + delta_row, self.col + delta_col)

    def move_by_direction(self, direction: Direction, steps: int = 1) -> "Position":
        """Create a new position moved by the given direction and steps"""
        return Position(
            self.row + direction.delta_row * steps,
            self.col + direction.delta_col * steps,
        )

    def __str__(self) -> str:
        """String representation of position"""
        return f"Position(row={self.row}, col={self.col})"
