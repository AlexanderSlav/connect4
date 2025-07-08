"""
Connect 4 Game - AI Player
Simple (Really dumb actually :) ) AI player with basic strategy
"""

import random
from typing import List, Optional
from src.enums import Player, GameState
from src.board import GameBoard


class AIPlayer:
    """Simple AI player with basic strategy"""
    
    def __init__(self, player: Player):
        self.player = player
        self.opponent = player.opposite()
    
    def get_move(self, board: GameBoard) -> Optional[int]:
        """Get AI move using simple strategy"""
        valid_moves = board.get_valid_moves()
        
        if not valid_moves:
            return None
        
        if random.random() < 0.3:
            return random.choice(valid_moves)
        
        win_move = self._find_winning_move(board, self.player)
        if win_move:
            return win_move
        
        block_move = self._find_winning_move(board, self.opponent)
        if block_move:
            return block_move
        
        return self._prefer_center_columns(valid_moves)
    
    def _find_winning_move(self, board: GameBoard, player: Player) -> Optional[int]:
        """Find a move that wins the game immediately"""
        valid_moves = board.get_valid_moves()
        
        for move in valid_moves:
            board.make_move(move, player)
            
            if board.check_winner() != GameState.PLAYING:
                board.undo_last_move()
                return move
            
            board.undo_last_move()
        
        return None
    
    def _prefer_center_columns(self, valid_moves: List[int]) -> int:
        """Prefer center columns for better strategic position"""
        if not valid_moves:
            return None
        
        center_col = (max(valid_moves) + min(valid_moves)) // 2
        sorted_moves = sorted(valid_moves, key=lambda x: abs(x - center_col))
        
        return sorted_moves[0]
    
    def get_player_symbol(self) -> str:
        """Get player symbol"""
        return self.player.symbol


class AIPlayerFactory:
    """Factory for creating AI players"""
    
    @staticmethod
    def create_ai_player() -> AIPlayer:
        """Create AI player (always YELLOW in single-player mode)"""
        return AIPlayer(Player.YELLOW) 