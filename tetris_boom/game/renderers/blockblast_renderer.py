import pygame
from game.renderers.base_renderer import BaseRenderer
from game.data import WHITE, RED, BLOCK_SIZE, DARK_BLOCK_COLORS, DARK_BLOCK_OUTLINE, LIGHT_BLOCK_COLORS, LIGHT_BLOCK_OUTLINE
from game.modes.base_mode import GameMode

class BlockBlastRenderer(BaseRenderer):
    def __init__(self, screen: pygame.Surface, game_mode: GameMode, dark_mode=False):
        super().__init__(screen, game_mode, dark_mode)

    def render(self):
        """
        Renders the game board, score, and next pieces for drag-and-drop
        """
        self.screen.fill(self.theme["background"])
        self._draw_game_board()
        self._draw_preview()
        self._draw_next_pieces()
        self._draw_dragging_block()
        self._draw_score()
        if self.game_mode.game_over:
            self._draw_game_over_message()
        pygame.display.flip()

    def _draw_next_pieces(self):
        start_x = self.offset_x + self.state.board.cols * BLOCK_SIZE + 50
        start_y = self.offset_y
        for index, block in enumerate(self.state.next_blocks[:3]):
            self.draw_block_at_screen_coords(block, start_x, start_y + index * 100)

    def compute_snapped_preview(self, block):
        """
        Compute snapped grid coordinates (x, y) for the dragged block.
        Ensures all filled cells stay on the board, and allows
        placement flush against any edge.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        board = self.state.board

        grid_x = round((mouse_x - self.offset_x) / BLOCK_SIZE)
        grid_y = round((mouse_y - self.offset_y) / BLOCK_SIZE)

        shape = block.get_shape()
        cells = [(k // 4, k % 4) for k in shape]

        min_j = min(j for i, j in cells)
        max_j = max(j for i, j in cells)
        min_i = min(i for i, j in cells)
        max_i = max(i for i, j in cells)

        grid_x -= min_j
        grid_y -= min_i

        if grid_x + min_j < 0:
            grid_x = -min_j
        if grid_y + min_i < 0:
            grid_y = -min_i
        if grid_x + max_j >= board.cols:
            grid_x = board.cols - 1 - max_j
        if grid_y + max_i >= board.rows:
            grid_y = board.rows - 1 - max_i

        return grid_x, grid_y

    def draw_block_at_screen_coords(self, block, screen_x, screen_y):
        """Draw a block at arbitrary screen coordinates (for next blocks / drag-and-drop)."""
        colors = DARK_BLOCK_COLORS if self.dark_mode else LIGHT_BLOCK_COLORS
        outline_color = self.theme["grid"]
        shape = block.get_shape()
        
        if block.is_bomb:
            block_color = self._get_bomb_color()
        else:
            block_color = colors[block.color_index]
        
        for i in range(4):
            for j in range(4):
                if i * 4 + j in shape:
                    x = screen_x + j * BLOCK_SIZE
                    y = screen_y + i * BLOCK_SIZE
                    pygame.draw.rect(
                        self.screen,
                        block_color,
                        [x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2]
                    )
                    pygame.draw.rect(
                        self.screen,
                        outline_color,
                        [x, y, BLOCK_SIZE, BLOCK_SIZE],
                        1
                    )
                    if block.is_bomb:
                        pygame.draw.rect(
                            self.screen,
                            RED,
                            [x, y, BLOCK_SIZE, BLOCK_SIZE],
                            2
                        )

    def _draw_dragging_block(self):
        handler = self.game_mode.input_handler
        block = handler.dragging_block

        if block:
            preview_x, preview_y = self.compute_snapped_preview(block)

            if (block.x != preview_x) or (block.y != preview_y):
                colors = DARK_BLOCK_COLORS if self.dark_mode else LIGHT_BLOCK_COLORS
                outline_color = DARK_BLOCK_OUTLINE if self.dark_mode else LIGHT_BLOCK_OUTLINE
                
                if block.is_bomb:
                    block_color = self._get_bomb_color()
                else:
                    block_color = colors[block.color_index]
                
                shape = block.get_shape()
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in shape:
                            rect = pygame.Rect(
                                self.offset_x + (preview_x + j) * BLOCK_SIZE + 1,
                                self.offset_y + (preview_y + i) * BLOCK_SIZE + 1,
                                BLOCK_SIZE - 2,
                                BLOCK_SIZE - 2
                            )
                            pygame.draw.rect(self.screen, block_color, rect)
                            pygame.draw.rect(self.screen, outline_color, rect, 1)
                            if block.is_bomb:
                                pygame.draw.rect(self.screen, RED, rect, 2)

    def _draw_preview(self):
        block = self.game_mode.input_handler.dragging_block
        if block:
            grid_x, grid_y = self.compute_snapped_preview(block)

            screen_x = self.offset_x + grid_x * BLOCK_SIZE
            screen_y = self.offset_y + grid_y * BLOCK_SIZE

            colors = DARK_BLOCK_COLORS if self.dark_mode else LIGHT_BLOCK_COLORS
            outline_color = DARK_BLOCK_OUTLINE if self.dark_mode else LIGHT_BLOCK_OUTLINE
            
            if block.is_bomb:
                block_color = self._get_bomb_color()
            else:
                block_color = colors[block.color_index]
            
            shape = block.get_shape()
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in shape:
                        rect = pygame.Rect(
                            screen_x + j * BLOCK_SIZE + 1,
                            screen_y + i * BLOCK_SIZE + 1,
                            BLOCK_SIZE - 2,
                            BLOCK_SIZE - 2
                        )
                        pygame.draw.rect(self.screen, block_color, rect)
                        pygame.draw.rect(self.screen, outline_color, rect, 1)
                        if block.is_bomb:
                            pygame.draw.rect(self.screen, RED, rect, 2)
