from abc import ABC, abstractmethod

from game.sound_manager import SoundManager

class BaseInputHandler(ABC):
    def __init__(self, game_mode):
        """
        Base input handler for all game modes.
        """
        self.game_mode = game_mode
        self.state = game_mode.state
        self.board = self.state.board
        self.sound_manager = SoundManager()

    @abstractmethod
    def handle(self, event):
        """
        Handle an input event.
        Subclasses must implement this.
        """
        pass

    def freeze_block(self, block):
        """
        Freeze the block on the board and update score.
        """
        self.board.freeze(block)
        lines_cleared = self.board.break_lines()
        self.state.score_manager.add_points(lines_cleared)

    def is_valid(self, block):
        """
        Check if the block's position is valid on the board.
        """
        return self.board.is_valid_position(block)
