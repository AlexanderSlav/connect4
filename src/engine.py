import time

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from config import GameConfig
from src.ai_player import AIPlayerFactory
from src.board import GameBoard
from src.consts import (
    AI_ERROR,
    AI_FALLBACK,
    AI_MOVE,
    AI_THINKING,
    ERROR_COLUMN_FULL,
    ERROR_GAME_INTERRUPTED,
    ERROR_INVALID_COLUMN,
    ERROR_UNKNOWN,
    GOODBYE_TEXT,
    PROMPT_PRESS_ENTER,
    PROMPT_START_GAME,
    SETUP_SINGLE_PLAYER,
    SETUP_TWO_PLAYER,
    WELCOME_TEXT,
    WIN_MESSAGES,
)
from src.enums import GameState, MoveResult, Player
from src.input_handler import InputHandler


class GameEngine:
    """Main game engine orchestrating the game flow"""

    def __init__(self, config: GameConfig = None):
        self.config = config or GameConfig()
        self.board = GameBoard(self.config)
        self.input_handler = InputHandler()
        self.console = Console()
        self.current_player = Player.RED
        self.game_state = GameState.PLAYING
        self.ai_player = None
        self.is_single_player = False

    def play(self) -> None:
        """Main game loop"""
        self.display_welcome()
        self.setup_game()

        while True:
            self.reset_game()

            while self.game_state == GameState.PLAYING:
                self.play_turn()

            self.display_result()

            if not self.input_handler.get_play_again_input():
                break

        self.display_goodbye()

    def play_turn(self) -> None:
        """Handle a single player turn"""
        self.board.display()

        if self.is_single_player and self.current_player == Player.YELLOW:
            self.play_ai_turn()
        else:
            self.play_human_turn()

        self.game_state = self.board.check_winner()

        if self.game_state == GameState.PLAYING:
            self.switch_player()

    def play_human_turn(self) -> None:
        """Handle human player turn"""
        while True:
            try:
                col = self.input_handler.get_column_input(
                    self.current_player, self.config.cols
                )

                result = self.board.make_move(col, self.current_player)

                if result == MoveResult.SUCCESS:
                    break
                elif result == MoveResult.COLUMN_FULL:
                    self.input_handler.display_error(ERROR_COLUMN_FULL.format(col))
                elif result == MoveResult.INVALID_COLUMN:
                    self.input_handler.display_error(
                        ERROR_INVALID_COLUMN.format(col, self.config.cols)
                    )
                else:
                    self.input_handler.display_error(ERROR_UNKNOWN)

            except KeyboardInterrupt:
                self.console.print(ERROR_GAME_INTERRUPTED, style="bold blue")
                raise

    def play_ai_turn(self) -> None:
        """Handle AI player turn"""
        self.console.print(f"\n{AI_THINKING}", end="")

        for _ in range(3):
            time.sleep(0.5)
            self.console.print(".", end="")

        ai_move = self.ai_player.get_move(self.board)

        if ai_move:
            result = self.board.make_move(ai_move, self.current_player)

            if result == MoveResult.SUCCESS:
                self.console.print(f"\n{AI_MOVE.format(ai_move)}", style="bold yellow")
                time.sleep(1)
            else:
                valid_moves = self.board.get_valid_moves()
                if valid_moves:
                    fallback_move = valid_moves[0]
                    self.board.make_move(fallback_move, self.current_player)
                    self.console.print(
                        f"\n{AI_FALLBACK.format(fallback_move)}", style="bold yellow"
                    )
        else:
            self.console.print(f"\n{AI_ERROR}", style="bold red")

    def switch_player(self) -> None:
        """Switch to the other player"""
        self.current_player = self.current_player.opposite()

    def display_welcome(self) -> None:
        """Display welcome message and instructions"""
        self.console.clear()

        title = Text("🔴 CONNECT 4 🟡", style="bold red")
        title.highlight_regex(r"🟡", "bold yellow")

        panel = Panel(
            Align.center(WELCOME_TEXT), title=title, border_style="blue", padding=(1, 2)
        )

        self.console.print(panel)
        self.input_handler.wait_for_enter(PROMPT_PRESS_ENTER)

    def setup_game(self) -> None:
        """Setup game mode"""
        game_mode = self.input_handler.get_game_mode_input()

        if game_mode == "one_player":
            self.is_single_player = True
            self.ai_player = AIPlayerFactory.create_ai_player()

            self.console.print(f"\n{SETUP_SINGLE_PLAYER}", style="bold green")

        else:
            self.is_single_player = False
            self.ai_player = None

            self.console.print(f"\n{SETUP_TWO_PLAYER}", style="bold green")

        self.input_handler.wait_for_enter(PROMPT_START_GAME)

    def display_result(self) -> None:
        """Display game result"""
        self.board.display()

        if self.game_state == GameState.RED_WINS:
            if self.is_single_player:
                result_text = Text(WIN_MESSAGES["human_win"], style="bold red")
            else:
                result_text = Text(WIN_MESSAGES["red_win"], style="bold red")
            winner_symbol = "🔴"
        elif self.game_state == GameState.YELLOW_WINS:
            if self.is_single_player:
                result_text = Text(WIN_MESSAGES["ai_win"], style="bold yellow")
            else:
                result_text = Text(WIN_MESSAGES["yellow_win"], style="bold yellow")
            winner_symbol = "🟡"
        elif self.game_state == GameState.DRAW:
            result_text = Text(WIN_MESSAGES["draw"], style="bold blue")
            winner_symbol = "🤝"
        else:
            result_text = Text(WIN_MESSAGES["unknown"], style="bold red")
            winner_symbol = "❓"

        panel = Panel(
            Align.center(result_text),
            title=f"Game Over {winner_symbol}",
            border_style="green" if self.game_state != GameState.DRAW else "blue",
            padding=(1, 2),
        )

        self.console.print(panel)

    def display_goodbye(self) -> None:
        """Display goodbye message"""
        goodbye_text = Text(GOODBYE_TEXT, style="bold blue")

        panel = Panel(
            Align.center(goodbye_text),
            title="Goodbye!",
            border_style="blue",
            padding=(1, 2),
        )

        self.console.print(panel)

    def reset_game(self) -> None:
        """Reset game for new round"""
        self.board.reset()
        self.current_player = Player.RED
        self.game_state = GameState.PLAYING

    def get_game_stats(self) -> dict:
        """Get current game statistics"""
        return {
            "board_size": f"{self.config.rows}x{self.config.cols}",
            "win_length": self.config.win_length,
            "current_player": self.current_player.name_str,
            "game_state": self.game_state.value,
            "moves_made": len(self.board.move_history),
            "valid_moves": self.board.get_valid_moves(),
        }
