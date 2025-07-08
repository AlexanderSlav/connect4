from typing import List, Optional, Tuple

from rich.align import Align
from rich.console import Console
from rich.table import Table

from config import GameConfig
from src.enums import Direction, GameState, MoveResult, Player, Position


class GameBoard:
    """Handles board state and operations"""

    def __init__(self, config: GameConfig):
        self.config = config
        self.board = [
            [Player.EMPTY for _ in range(config.cols)] for _ in range(config.rows)
        ]
        self.console = Console()
        self.move_history: List[Tuple[Position, Player]] = []  # (position, player)

    def display(self) -> None:
        """Display the current board state"""
        table = Table(show_header=True, header_style="bold blue")

        for col in range(1, self.config.cols + 1):
            table.add_column(str(col), justify="center", style="cyan", width=3)

        for row in range(self.config.rows):
            row_data = []
            for col in range(self.config.cols):
                cell = self.board[row][col]
                if cell == Player.EMPTY:
                    row_data.append("⚪")
                else:
                    row_data.append(cell.symbol)
            table.add_row(*row_data)

        self.console.print()
        self.console.print(Align.center(table))
        self.console.print()

    def is_valid_move(self, col: int) -> bool:
        """Check if a move is valid"""
        col_idx = col - 1

        if col_idx < 0 or col_idx >= self.config.cols:
            return False

        return self.board[0][col_idx] == Player.EMPTY

    def make_move(self, col: int, player: Player) -> MoveResult:
        """Make a move on the board"""
        col_idx = col - 1

        if not self.is_valid_move(col):
            if col_idx < 0 or col_idx >= self.config.cols:
                return MoveResult.INVALID_COLUMN
            else:
                return MoveResult.COLUMN_FULL

        for row in range(self.config.rows - 1, -1, -1):
            if self.board[row][col_idx] == Player.EMPTY:
                self.board[row][col_idx] = player
                position = Position(row, col_idx)
                self.move_history.append((position, player))
                return MoveResult.SUCCESS

        return MoveResult.COLUMN_FULL

    def check_winner(self) -> GameState:
        """Check if there's a winner or draw"""
        winner = self._find_winner_on_board()
        if winner:
            return self._player_to_game_state(winner)

        if self.is_full():
            return GameState.DRAW

        return GameState.PLAYING

    def _find_winner_on_board(self) -> Optional[Player]:
        """Scan the entire board to find a winning player"""
        for row in range(self.config.rows):
            for col in range(self.config.cols):
                position = Position(row, col)
                if self._is_occupied_position(position):
                    winner = self._check_all_directions_from_position(position)
                    if winner:
                        return winner
        return None

    def _is_occupied_position(self, position: Position) -> bool:
        """Check if a board position is occupied by a player"""
        return self.board[position.row][position.col] != Player.EMPTY

    def _check_all_directions_from_position(
        self, position: Position
    ) -> Optional[Player]:
        """Check all possible winning directions from a given position"""
        for direction in Direction:
            winner = self._check_line(position, direction)
            if winner and winner != Player.EMPTY:
                return winner
        return None

    def _player_to_game_state(self, player: Player) -> GameState:
        """Convert a winning player to the corresponding game state"""
        player_to_state = {
            Player.RED: GameState.RED_WINS,
            Player.YELLOW: GameState.YELLOW_WINS,
        }
        return player_to_state.get(player, GameState.PLAYING)

    def _check_line(
        self, start_position: Position, direction: Direction
    ) -> Optional[Player]:
        """Helper method to check a line for winner"""
        player = self.board[start_position.row][start_position.col]

        if player == Player.EMPTY:
            return None

        count = 1

        # Check in both directions
        for direction_multiplier in [1, -1]:
            current_pos = start_position.move_by_direction(
                direction, direction_multiplier
            )

            while (
                current_pos.is_valid(self.config.rows, self.config.cols)
                and self.board[current_pos.row][current_pos.col] == player
            ):
                count += 1
                current_pos = current_pos.move_by_direction(
                    direction, direction_multiplier
                )

        return player if count >= self.config.win_length else None

    def is_full(self) -> bool:
        """Check if board is full"""
        return all(
            self.board[0][col] != Player.EMPTY for col in range(self.config.cols)
        )

    def get_valid_moves(self) -> List[int]:
        """Get list of valid column numbers (1-based)"""
        return [
            col + 1 for col in range(self.config.cols) if self.is_valid_move(col + 1)
        ]

    def reset(self) -> None:
        """Reset the board to initial state"""
        self.board = [
            [Player.EMPTY for _ in range(self.config.cols)]
            for _ in range(self.config.rows)
        ]
        self.move_history.clear()

    def get_board_copy(self) -> List[List[Player]]:
        """Get a copy of the current board state"""
        return [row[:] for row in self.board]

    def undo_last_move(self) -> bool:
        """Undo the last move"""
        if not self.move_history:
            return False

        position, player = self.move_history.pop()
        self.board[position.row][position.col] = Player.EMPTY
        return True

    def get_column_height(self, col: int) -> int:
        """Get the number of pieces in a column (1-based column number)"""
        col_idx = col - 1
        if col_idx < 0 or col_idx >= self.config.cols:
            return 0

        count = 0
        for row in range(self.config.rows):
            if self.board[row][col_idx] != Player.EMPTY:
                count += 1
        return count
