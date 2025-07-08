
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
    
    def opposite(self) -> 'Player':
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