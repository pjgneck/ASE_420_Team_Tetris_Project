import pygame
from game.renderers.base_renderer import BaseRenderer
from game.data import WHITE, BLOCK_SIZE

class TetrisRenderer(BaseRenderer):
    def __init__(self, screen, game_mode):
        super().__init__(screen, game_mode)

    def render(self):
        self.screen.fill(WHITE)
        self._draw_game_board()
        self._draw_current_block()
        self._draw_score()

        if self.game_mode.game_over:
            self._draw_game_over_message()

        pygame.display.flip()

    def _draw_current_block(self):
        """
        Draws the current falling block at its position on the board.
        Works with flat-index SHAPES (0-15 for 4x4 grid or larger for bigger shapes).
        """
        current_block = self.state.current_block
        shape_indices = current_block.get_shape()  # e.g. [1, 5, 9, 13]

        for idx in shape_indices:
            # Compute row and column inside the block's local grid
            r = idx // 4  # each shape is at most 4 columns wide in the SHAPES definition
            c = idx % 4

            # Compute actual position on the board
            x = current_block.x + c
            y = current_block.y + r

            pygame.draw.rect(
                self.screen,
                current_block.get_color(),
                [
                    self.offset_x + x * BLOCK_SIZE + 1,
                    self.offset_y + y * BLOCK_SIZE + 1,
                    BLOCK_SIZE - 2,
                    BLOCK_SIZE - 2
                ]
            )
