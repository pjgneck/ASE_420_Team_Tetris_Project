from game.score_manager import ScoreManager
from game.sound_manager import SoundManager
from game.board import Board
from game.block_factory import BlockFactory

class GameState:
    def __init__(self, board: Board, block_factory: BlockFactory, score_manager: ScoreManager, sound_manager: SoundManager):
        self.board = board
        self.block_factory = block_factory
        self.score_manager = score_manager
        self.sound_manager = sound_manager
        self.current_block = self.block_factory.create_block()
        self.next_blocks = []
        self.selected_block = None
        self.preview_position = None
        self.game_over = False
