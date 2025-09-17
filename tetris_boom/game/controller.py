from game.modes.base import GameMode
from game.score import ScoreManager
from game.board import Board
from game.input_handler import InputHandler
from game.renderer import Renderer
from game.modes.tetris import TetrisMode

class GameController:
    def __init__(self):
        self.score_manager = ScoreManager()
        self.board = Board()
        self.input_handler = InputHandler()
        self.renderer = Renderer()
        self.current_mode: GameMode = TetrisMode(self.board, self.score_manager)

    def run_game_loop(self):
        running = True
        while running:
            self.input_handler.process_input()
            self.current_mode.handle_input()
            self.current_mode.update()
            self.current_mode.render(self.renderer)

            if self.score_manager.should_switch():
                self.switch_mode()

    def switch_mode(self):
        # placeholder for switching between TetrisMode and BlockBlastMode
        pass
