import pygame
from game.input_handlers.base_input_handler import BaseInputHandler

class TetrisInputHandler(BaseInputHandler):
    def __init__(self, tetris_mode):
        super().__init__(tetris_mode)
        self.tetris_mode = tetris_mode  # For pressing_down and game_over flags

    def handle(self, event):
        block = self.state.current_block
        factory = self.state.block_factory

        if event.type == pygame.KEYDOWN:
            # Quit game if game over
            if self.tetris_mode.game_over and event.key == pygame.K_q:
                return "quit"

            # Move left
            if event.key == pygame.K_LEFT:
                block.move(-1, 0)
                if not self.is_valid(block):
                    block.move(1, 0)

            # Move right
            elif event.key == pygame.K_RIGHT:
                block.move(1, 0)
                if not self.is_valid(block):
                    block.move(-1, 0)

            # Soft drop
            elif event.key == pygame.K_DOWN:
                self.tetris_mode.pressing_down = True

            # Rotate
            elif event.key == pygame.K_UP:
                block.rotate()
                if not self.is_valid(block):
                    block.undo_rotate()

            # Hard drop
            elif event.key == pygame.K_SPACE:
                while self.is_valid(block):
                    block.move(0, 1)
                block.move(0, -1)
                self.freeze_block(block)

                # Spawn new block
                self.state.current_block = factory.create_block()

                # Check for game over
                if not self.is_valid(self.state.current_block):
                    self.tetris_mode.game_over = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.tetris_mode.pressing_down = False
