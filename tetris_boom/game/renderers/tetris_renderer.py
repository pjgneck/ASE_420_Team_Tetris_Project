import pygame
from game.renderers.base_renderer import BaseRenderer
from game.data import WHITE, BLOCK_SIZE, DARK_BLOCK_OUTLINE, DARK_BLOCK_COLORS, LIGHT_BLOCK_COLORS, LIGHT_BLOCK_OUTLINE
from game.modes.base_mode import GameMode

class TetrisRenderer(BaseRenderer):
    def __init__(self, screen: pygame.Surface, game_mode: GameMode, dark_mode=False):
        super().__init__(screen, game_mode, dark_mode)

    def render(self):
        self.screen.fill(self.theme["background"])
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
        shape_indices = current_block.get_shape()
        colors = DARK_BLOCK_COLORS if self.dark_mode else LIGHT_BLOCK_COLORS

        for idx in shape_indices:
            r = idx // 4
            c = idx % 4

            x = current_block.x + c
            y = current_block.y + r
            color = current_block.get_color(colors)

            pygame.draw.rect(
                self.screen,
                color,
                [
                    self.offset_x + x * BLOCK_SIZE + 1,
                    self.offset_y + y * BLOCK_SIZE + 1,
                    BLOCK_SIZE - 2,
                    BLOCK_SIZE - 2
                ]
            )
