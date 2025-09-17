import pygame
from game.board import Board
from game.piece_factory import PieceFactory
from game.score import ScoreManager
from game.modes.base import GameMode

class TetrisMode(GameMode):
    def __init__(self, screen, input_handler, renderer):
        self.screen = screen
        self.board = Board()
        self.factory = PieceFactory()
        self.block = self.factory.create_block()
        self.score = ScoreManager()
        self.game_over = False
        self.gravity = 1.0  # blocks per second
        self.fall_timer = 0.0
        self.pressing_down = False
        # Injected classes — will create instances below
        self.input_handler = input_handler(self)
        self.renderer = renderer(screen, self)

    def update(self):
        if self.game_over:
            return

        # Time-based falling
        dt = 1 / 30  # Assuming game loop runs at 30 FPS
        self.fall_timer += dt

        # Calculate drop interval based on gravity
        drop_interval = 1.0 / self.gravity

        if self.fall_timer >= drop_interval or self.pressing_down:
            self.block.move(0, 1)

            if not self.board.is_valid_position(self.block):
                # Revert the move and lock the block
                self.block.move(0, -1)
                self.board.freeze(self.block)

                lines_cleared = self.board.break_lines()
                self.score.update(lines_cleared)

                self.block = self.factory.create_block()

                if not self.board.is_valid_position(self.block):
                    self.game_over = True

            self.fall_timer = 0.0  # Reset timer after a move


    def handle_input(self, event):
        return self.input_handler.handle(event)

    def render(self):
        self.renderer.render()

    def spawn_piece(self):
        self.block = self.factory.create_block()
