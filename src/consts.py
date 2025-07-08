WELCOME_TEXT = """
Welcome to Connect 4!

🎯 OBJECTIVE:
Be the first player to get 4 of your pieces in a row!

🎮 HOW TO PLAY:
• Players take turns dropping pieces into columns
• Pieces fall to the lowest empty space in the column
• Get 4 in a row horizontally, vertically, or diagonally to win!

🔴 Red player goes first
🟡 Yellow player goes second (or AI in single-player mode)

Good luck and have fun!
"""

GOODBYE_TEXT = "👋 Thanks for playing Connect 4! See you next time!"

GAME_MODE_PROMPT = """
🎮 Select Game Mode:
1. Two Player - Play against another human
2. Single Player - Play against AI

Enter choice (1 or 2): """

SETUP_SINGLE_PLAYER = """✅ Game Setup Complete!
   Mode: Single Player vs AI
   You are: Red Player 🔴
   AI is: Yellow Player 🟡"""

SETUP_TWO_PLAYER = """✅ Game Setup Complete!
   Mode: Two Player
   Player 1: Red Player 🔴
   Player 2: Yellow Player 🟡"""

WIN_MESSAGES = {
    "human_win": "🎉 YOU WIN! 🎉",
    "ai_win": "🤖 AI WINS! 🤖", 
    "red_win": "🎉 RED PLAYER WINS! 🎉",
    "yellow_win": "🎉 YELLOW PLAYER WINS! 🎉",
    "draw": "🤝 IT'S A DRAW! 🤝",
    "unknown": "❓ UNKNOWN RESULT"
}

AI_THINKING = "🤖 AI is thinking"
AI_MOVE = "🤖 AI chooses column {}"
AI_FALLBACK = "🤖 AI chooses column {} (fallback)"
AI_ERROR = "❌ AI couldn't find a move!"

ERROR_COLUMN_FULL = "Column {} is full! Choose another column."
ERROR_INVALID_COLUMN = "Invalid column {}! Choose a column between 1 and {}."
ERROR_UNKNOWN = "Unknown error occurred. Please try again."
ERROR_GAME_INTERRUPTED = "\n\n👋 Thanks for playing Connect 4!"

ERROR_ENTER_NUMBER = "❌ Please enter a column number!"
ERROR_VALID_NUMBER = "❌ Please enter a valid number!"
ERROR_COLUMN_RANGE = "❌ Column must be between 1 and {}!"
ERROR_ENTER_Y_OR_N = "❌ Please enter 'y' for yes or 'n' for no!"
ERROR_ENTER_1_OR_2 = "❌ Please enter 1 or 2!"

PROMPT_PLAY_AGAIN = "\n🎮 Do you want to play again? (y/n): "
PROMPT_PRESS_ENTER = "Press Enter to continue..."
PROMPT_START_GAME = "Press Enter to start the game..."