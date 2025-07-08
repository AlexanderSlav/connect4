
from src.enums import Player
from rich.console import Console
from rich.text import Text
from src.consts import (
    GAME_MODE_PROMPT, ERROR_ENTER_NUMBER, ERROR_VALID_NUMBER, 
    ERROR_COLUMN_RANGE, ERROR_ENTER_Y_OR_N, ERROR_ENTER_1_OR_2,
    PROMPT_PLAY_AGAIN, ERROR_GAME_INTERRUPTED
)


class InputHandler:
    """Handles user input with validation"""
    
    def __init__(self):
        self.console = Console()
    
    def get_column_input(self, current_player: Player, max_cols: int) -> int:
        """Get and validate column input from user"""
        while True:
            try:
                player_text = Text()
                player_text.append(f"Player {current_player.symbol} ({current_player.name_str.upper()})", 
                                 style="bold red" if current_player == Player.RED else "bold yellow")
                
                self.console.print(player_text, end="")
                self.console.print(f", enter column (1-{max_cols}): ", end="")
                
                user_input = input().strip()
                
                if not user_input:
                    self.console.print(ERROR_ENTER_NUMBER, style="bold red")
                    continue
                
                try:
                    col = int(user_input)
                except ValueError:
                    self.console.print(ERROR_VALID_NUMBER, style="bold red")
                    continue
                
                if col < 1 or col > max_cols:
                    self.console.print(ERROR_COLUMN_RANGE.format(max_cols), style="bold red")
                    continue
                
                return col
                
            except KeyboardInterrupt:
                self.console.print(ERROR_GAME_INTERRUPTED, style="bold red")
                raise
            except EOFError:
                self.console.print("\n❌ End of input reached!", style="bold red")
                raise
    
    def get_play_again_input(self) -> bool:
        """Ask if players want to play again"""
        while True:
            try:
                self.console.print(PROMPT_PLAY_AGAIN, style="bold blue", end="")
                user_input = input().strip().lower()
                
                if user_input in ['y', 'yes', '1', 'true']:
                    return True
                elif user_input in ['n', 'no', '0', 'false']:
                    return False
                else:
                    self.console.print(ERROR_ENTER_Y_OR_N, style="bold red")
                    continue
                    
            except KeyboardInterrupt:
                self.console.print(ERROR_GAME_INTERRUPTED, style="bold red")
                return False
            except EOFError:
                self.console.print("\n❌ End of input reached!", style="bold red")
                return False
    
    def display_message(self, message: str, style: str = "bold white") -> None:
        """Display a message with styling"""
        self.console.print(message, style=style)
    
    def display_error(self, error_message: str) -> None:
        """Display an error message"""
        self.console.print(f"❌ {error_message}", style="bold red")
    
    def display_success(self, success_message: str) -> None:
        """Display a success message"""
        self.console.print(f"✅ {success_message}", style="bold green")
    
    def display_info(self, info_message: str) -> None:
        """Display an info message"""
        self.console.print(f"ℹ️  {info_message}", style="bold blue")
    
    def clear_screen(self) -> None:
        """Clear the console screen"""
        self.console.clear()
    
    def wait_for_enter(self, message: str = "Press Enter to continue...") -> None:
        """Wait for user to press Enter"""
        try:
            self.console.print(f"\n{message}", style="dim")
            input()
        except KeyboardInterrupt:
            pass
    
    def get_game_mode_input(self) -> str:
        """Get game mode selection from user"""
        while True:
            try:
                self.console.print(GAME_MODE_PROMPT, end="")
                
                user_input = input().strip()
                
                if user_input == "1":
                    return "two_player"
                elif user_input == "2":
                    return "one_player"
                else:
                    self.console.print(ERROR_ENTER_1_OR_2, style="bold red")
                    continue
                    
            except KeyboardInterrupt:
                self.console.print(ERROR_GAME_INTERRUPTED, style="bold red")
                raise
            except EOFError:
                self.console.print("\n❌ End of input reached!", style="bold red")
                raise
    

