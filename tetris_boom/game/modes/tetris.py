from game.modes.base import GameMode
from game.board import Board
from game.score import ScoreManager
from game.piece_factory import PieceFactory

class TetrisMode(GameMode):
    def __init__(self, board: Board, score_manager: ScoreManager):
        self.board = board
        self.score_manager = score_manager
        self.piece_factory = PieceFactory()
        self.current_piece = self.spawn_piece()

    def update(self):
        pass  # Apply gravity, check for line clears, etc.

    def handle_input(self):
        pass  # Handle keyboard events for piece movement

    def render(self, renderer):
        renderer.draw_board(self.board)
        renderer.draw_piece(self.current_piece)

    def spawn_piece(self):
        return self.piece_factory.create_piece()
