from unittest.mock import patch

import pytest

from config import GameConfig
from src.board import GameBoard
from src.enums import Direction, GameState, MoveResult, Player, Position


class TestGameBoard:
    """Test suite for GameBoard class"""

    @pytest.fixture
    def default_config(self):
        """Default configuration for testing"""
        return GameConfig(rows=6, cols=7, win_length=4)

    @pytest.fixture
    def small_config(self):
        """Small board configuration for testing"""
        return GameConfig(rows=4, cols=4, win_length=3)

    @pytest.fixture
    def board(self, default_config):
        """Default board instance"""
        return GameBoard(default_config)

    @pytest.fixture
    def small_board(self, small_config):
        """Small board instance"""
        return GameBoard(small_config)

    def test_init(self, default_config):
        """Test board initialization"""
        board = GameBoard(default_config)
        assert board.config == default_config
        assert len(board.board) == 6
        assert len(board.board[0]) == 7
        assert all(cell == Player.EMPTY for row in board.board for cell in row)
        assert board.move_history == []

    def test_is_valid_move_valid_columns(self, board):
        """Test valid move validation"""
        # Test valid columns (1-based)
        for col in range(1, 8):
            assert board.is_valid_move(col) is True

    def test_is_valid_move_invalid_columns(self, board):
        """Test invalid column validation"""
        # Test invalid columns
        assert board.is_valid_move(0) is False
        assert board.is_valid_move(8) is False
        assert board.is_valid_move(-1) is False
        assert board.is_valid_move(100) is False

    def test_is_valid_move_full_column(self, small_board):
        """Test validation when column is full"""
        # Fill column 1 completely
        for _ in range(4):
            result = small_board.make_move(1, Player.RED)
            assert result == MoveResult.SUCCESS

        # Column should now be invalid
        assert small_board.is_valid_move(1) is False

    def test_make_move_success(self, board):
        """Test successful move"""
        result = board.make_move(1, Player.RED)
        assert result == MoveResult.SUCCESS
        assert board.board[5][0] == Player.RED  # Bottom row, first column
        assert len(board.move_history) == 1
        position, player = board.move_history[0]
        assert position == Position(5, 0)
        assert player == Player.RED

    def test_make_move_gravity_effect(self, board):
        """Test gravity effect in moves"""
        # Make multiple moves in the same column
        board.make_move(1, Player.RED)
        board.make_move(1, Player.YELLOW)
        board.make_move(1, Player.RED)

        # Check pieces stack correctly
        assert board.board[5][0] == Player.RED
        assert board.board[4][0] == Player.YELLOW
        assert board.board[3][0] == Player.RED

    def test_make_move_invalid_column(self, board):
        """Test move with invalid column"""
        assert board.make_move(0, Player.RED) == MoveResult.INVALID_COLUMN
        assert board.make_move(8, Player.RED) == MoveResult.INVALID_COLUMN
        assert board.make_move(-1, Player.RED) == MoveResult.INVALID_COLUMN

    def test_make_move_column_full(self, small_board):
        """Test move when column is full"""
        # Fill column 1 completely
        for _ in range(4):
            small_board.make_move(1, Player.RED)

        # Next move should fail
        result = small_board.make_move(1, Player.YELLOW)
        assert result == MoveResult.COLUMN_FULL

    def test_check_winner_horizontal(self, board):
        """Test horizontal win detection"""
        # Create horizontal win for RED
        for col in range(1, 5):
            board.make_move(col, Player.RED)

        assert board.check_winner() == GameState.RED_WINS

    def test_check_winner_vertical(self, board):
        """Test vertical win detection"""
        # Create vertical win for YELLOW
        for _ in range(4):
            board.make_move(1, Player.YELLOW)

        assert board.check_winner() == GameState.YELLOW_WINS

    def test_check_winner_diagonal_right(self, board):
        """Test diagonal (right) win detection"""
        # Create diagonal win: /
        # Column 1: 1 RED
        # Column 2: 1 YELLOW, 1 RED
        # Column 3: 2 YELLOW, 1 RED
        # Column 4: 3 YELLOW, 1 RED

        board.make_move(1, Player.RED)

        board.make_move(2, Player.YELLOW)
        board.make_move(2, Player.RED)

        board.make_move(3, Player.YELLOW)
        board.make_move(3, Player.YELLOW)
        board.make_move(3, Player.RED)

        board.make_move(4, Player.YELLOW)
        board.make_move(4, Player.YELLOW)
        board.make_move(4, Player.YELLOW)
        board.make_move(4, Player.RED)

        assert board.check_winner() == GameState.RED_WINS

    def test_check_winner_diagonal_left(self, board):
        """Test diagonal (left) win detection"""
        # Create diagonal win: \
        # Column 4: 1 RED
        # Column 3: 1 YELLOW, 1 RED
        # Column 2: 2 YELLOW, 1 RED
        # Column 1: 3 YELLOW, 1 RED

        board.make_move(4, Player.RED)

        board.make_move(3, Player.YELLOW)
        board.make_move(3, Player.RED)

        board.make_move(2, Player.YELLOW)
        board.make_move(2, Player.YELLOW)
        board.make_move(2, Player.RED)

        board.make_move(1, Player.YELLOW)
        board.make_move(1, Player.YELLOW)
        board.make_move(1, Player.YELLOW)
        board.make_move(1, Player.RED)

        assert board.check_winner() == GameState.RED_WINS

    def test_check_winner_no_winner(self, board):
        """Test no winner state"""
        # Make some moves but no win
        board.make_move(1, Player.RED)
        board.make_move(2, Player.YELLOW)
        board.make_move(3, Player.RED)

        assert board.check_winner() == GameState.PLAYING

    def test_check_winner_draw(self, small_board):
        """Test draw detection"""
        # Fill the board in an alternating pattern that prevents any 3-in-a-row:
        # RED    YELLOW YELLOW RED
        # YELLOW RED    RED    YELLOW
        # RED    YELLOW YELLOW RED
        # YELLOW RED    RED    YELLOW
        moves = [
            # Bottom row: YELLOW RED RED YELLOW
            (1, Player.YELLOW),
            (2, Player.RED),
            (3, Player.RED),
            (4, Player.YELLOW),
            # Third row: RED YELLOW YELLOW RED
            (1, Player.RED),
            (2, Player.YELLOW),
            (3, Player.YELLOW),
            (4, Player.RED),
            # Second row: YELLOW RED RED YELLOW
            (1, Player.YELLOW),
            (2, Player.RED),
            (3, Player.RED),
            (4, Player.YELLOW),
            # Top row: RED YELLOW YELLOW RED
            (1, Player.RED),
            (2, Player.YELLOW),
            (3, Player.YELLOW),
            (4, Player.RED),
        ]

        for col, player in moves:
            small_board.make_move(col, player)

        assert small_board.check_winner() == GameState.DRAW

    def test_is_full_empty_board(self, board):
        """Test is_full on empty board"""
        assert board.is_full() is False

    def test_is_full_partial_board(self, board):
        """Test is_full on partially filled board"""
        board.make_move(1, Player.RED)
        board.make_move(2, Player.YELLOW)
        assert board.is_full() is False

    def test_is_full_full_board(self, small_board):
        """Test is_full on completely filled board"""
        # Fill all columns
        for col in range(1, 5):
            for _ in range(4):
                small_board.make_move(col, Player.RED)

        assert small_board.is_full() is True

    def test_get_valid_moves_empty_board(self, board):
        """Test get_valid_moves on empty board"""
        valid_moves = board.get_valid_moves()
        assert valid_moves == [1, 2, 3, 4, 5, 6, 7]

    def test_get_valid_moves_partial_board(self, small_board):
        """Test get_valid_moves on partially filled board"""
        # Fill column 1 and 2
        for _ in range(4):
            small_board.make_move(1, Player.RED)
            small_board.make_move(2, Player.YELLOW)

        valid_moves = small_board.get_valid_moves()
        assert valid_moves == [3, 4]

    def test_reset(self, board):
        """Test board reset"""
        # Make some moves
        board.make_move(1, Player.RED)
        board.make_move(2, Player.YELLOW)

        # Reset board
        board.reset()

        # Check everything is cleared
        assert all(cell == Player.EMPTY for row in board.board for cell in row)
        assert board.move_history == []

    def test_get_board_copy(self, board):
        """Test get_board_copy"""
        board.make_move(1, Player.RED)
        board_copy = board.get_board_copy()

        # Modify copy
        board_copy[0][0] = Player.YELLOW

        # Original should be unchanged
        assert board.board[0][0] == Player.EMPTY
        assert board.board[5][0] == Player.RED

    def test_undo_last_move(self, board):
        """Test undo functionality"""
        # Make a move
        board.make_move(1, Player.RED)
        assert board.board[5][0] == Player.RED
        assert len(board.move_history) == 1

        # Undo move
        success = board.undo_last_move()
        assert success is True
        assert board.board[5][0] == Player.EMPTY
        assert len(board.move_history) == 0

    def test_undo_last_move_empty_history(self, board):
        """Test undo when no moves made"""
        success = board.undo_last_move()
        assert success is False

    def test_get_column_height(self, board):
        """Test get_column_height"""
        # Empty column
        assert board.get_column_height(1) == 0

        # Add pieces
        board.make_move(1, Player.RED)
        board.make_move(1, Player.YELLOW)
        assert board.get_column_height(1) == 2

        # Invalid column
        assert board.get_column_height(0) == 0
        assert board.get_column_height(8) == 0

    def test_display(self, board):
        """Test console display"""
        with patch.object(board.console, "print") as mock_print:
            board.display()
            assert mock_print.call_count == 3  # Empty line, table, empty line

    def test_custom_win_length(self):
        """Test custom win length configuration"""
        config = GameConfig(rows=6, cols=7, win_length=5)
        board = GameBoard(config)

        # Create 4 in a row (should not win with win_length=5)
        for col in range(1, 5):
            board.make_move(col, Player.RED)

        assert board.check_winner() == GameState.PLAYING

        # Add 5th piece
        board.make_move(5, Player.RED)
        assert board.check_winner() == GameState.RED_WINS


class TestEnums:
    """Test suite for enum enhancements"""

    def test_player_properties(self):
        """Test Player enum properties"""
        assert Player.RED.symbol == "🔴"
        assert Player.YELLOW.symbol == "🟡"
        assert Player.EMPTY.symbol == "⚪"

        assert Player.RED.name_str == "red"
        assert Player.YELLOW.name_str == "yellow"
        assert Player.EMPTY.name_str == "empty"

    def test_player_opposite(self):
        """Test Player.opposite method"""
        assert Player.RED.opposite() == Player.YELLOW
        assert Player.YELLOW.opposite() == Player.RED
        assert Player.EMPTY.opposite() == Player.EMPTY

    def test_game_state_properties(self):
        """Test GameState enum properties"""
        assert GameState.PLAYING.is_game_over is False
        assert GameState.RED_WINS.is_game_over is True
        assert GameState.YELLOW_WINS.is_game_over is True
        assert GameState.DRAW.is_game_over is True

    def test_direction_properties(self):
        """Test Direction enum properties"""
        assert Direction.HORIZONTAL.delta_row == 0
        assert Direction.HORIZONTAL.delta_col == 1

        assert Direction.VERTICAL.delta_row == 1
        assert Direction.VERTICAL.delta_col == 0

        assert Direction.DIAGONAL_RIGHT.delta_row == 1
        assert Direction.DIAGONAL_RIGHT.delta_col == 1

        assert Direction.DIAGONAL_LEFT.delta_row == 1
        assert Direction.DIAGONAL_LEFT.delta_col == -1

    def test_move_result_enum(self):
        """Test MoveResult enum values"""
        assert MoveResult.SUCCESS.value == "success"
        assert MoveResult.INVALID_COLUMN.value == "invalid_column"
        assert MoveResult.COLUMN_FULL.value == "column_full"
        assert MoveResult.GAME_OVER.value == "game_over"

    def test_position_creation(self):
        """Test Position creation and basic properties"""
        pos = Position(2, 3)
        assert pos.row == 2
        assert pos.col == 3
        assert str(pos) == "Position(row=2, col=3)"

    def test_position_validation(self):
        """Test Position validation"""
        # Valid positions
        assert Position(0, 0).is_valid(6, 7) is True
        assert Position(2, 3).is_valid(6, 7) is True
        assert Position(5, 6).is_valid(6, 7) is True

        # Invalid positions
        assert Position(6, 3).is_valid(6, 7) is False  # row out of bounds
        assert Position(2, 7).is_valid(6, 7) is False  # col out of bounds
        assert Position(-1, 3).is_valid(6, 7) is False  # negative row
        assert Position(2, -1).is_valid(6, 7) is False  # negative col

    def test_position_move_by(self):
        """Test Position move_by method"""
        pos = Position(2, 3)
        new_pos = pos.move_by(1, -1)
        assert new_pos.row == 3
        assert new_pos.col == 2
        assert pos.row == 2  # Original should be unchanged
        assert pos.col == 3

    def test_position_move_by_direction(self):
        """Test Position move_by_direction method"""
        pos = Position(2, 3)

        # Move horizontally
        new_pos = pos.move_by_direction(Direction.HORIZONTAL, 2)
        assert new_pos.row == 2
        assert new_pos.col == 5

        # Move vertically
        new_pos = pos.move_by_direction(Direction.VERTICAL, 3)
        assert new_pos.row == 5
        assert new_pos.col == 3

        # Move diagonally
        new_pos = pos.move_by_direction(Direction.DIAGONAL_RIGHT, 2)
        assert new_pos.row == 4
        assert new_pos.col == 5

    def test_position_negative_coordinates(self):
        """Test Position with negative coordinates (allowed for algorithm flexibility)"""
        # Negative coordinates are allowed during creation for algorithm flexibility
        pos1 = Position(-1, 0)
        pos2 = Position(0, -1)
        pos3 = Position(-1, -1)

        # But they should be invalid for any board size
        assert pos1.is_valid(6, 7) is False
        assert pos2.is_valid(6, 7) is False
        assert pos3.is_valid(6, 7) is False

    def test_position_equality(self):
        """Test Position equality"""
        pos1 = Position(2, 3)
        pos2 = Position(2, 3)
        pos3 = Position(3, 2)

        assert pos1 == pos2
        assert pos1 != pos3
        assert pos2 != pos3

    def test_position_immutability(self):
        """Test that Position is immutable (frozen dataclass)"""
        pos = Position(2, 3)

        # Should not be able to modify
        with pytest.raises(AttributeError):
            pos.row = 5

        with pytest.raises(AttributeError):
            pos.col = 7


if __name__ == "__main__":
    pytest.main([__file__])
