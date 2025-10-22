import pygame
from game.block_data import WHITE, GRAY, BLACK, ORANGE, BLOCK_SIZE

class BlockBlastRenderer:
    def __init__(self, screen, game_mode):
        """
        Renderer for BlockBlastMode
        :param screen: Pygame display surface
        :param game_mode: BlockBlastMode instance
        """
        self.screen = screen
        self.game_mode = game_mode
        self.state = game_mode.state  # shared GameState

        # Board offsets (same as Tetris)
        board = self.state.board
        self.offset_x = (screen.get_width() - board.cols * BLOCK_SIZE) // 2
        self.offset_y = (screen.get_height() - board.rows * BLOCK_SIZE) // 2

        # Fonts
        self.font = pygame.font.SysFont('Calibri', 20, True)
        self.large_font = pygame.font.SysFont('Calibri', 35, True)

    def render(self):
        """
        Renders the game board, score, and next pieces for drag-and-drop
        """
        self.screen.fill(WHITE)
        self._draw_game_board()
        self._draw_preview()
        self._draw_next_pieces()
        self._draw_dragging_block()
        self._draw_score()
        if self.game_mode.game_over:
            self._draw_game_over_message()
        pygame.display.flip()

    def _draw_game_board(self):
        """
        Draws the board grid and frozen blocks (no falling block)
        """
        board = self.state.board
        for row in range(board.rows):
            for col in range(board.cols):
                block_value = board.grid[row][col]
                if block_value > 0:
                    pygame.draw.rect(
                        self.screen,
                        board.BLOCK_COLORS[block_value],
                        [
                            self.offset_x + col * BLOCK_SIZE + 1,
                            self.offset_y + row * BLOCK_SIZE + 1,
                            BLOCK_SIZE - 2,
                            BLOCK_SIZE - 2
                        ]
                    )
                # Draw grid
                pygame.draw.rect(
                    self.screen,
                    GRAY,
                    [
                        self.offset_x + col * BLOCK_SIZE,
                        self.offset_y + row * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    ],
                    1
                )

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

        # Mouse in grid coords (round to nearest cell)
        grid_x = round((mouse_x - self.offset_x) / BLOCK_SIZE)
        grid_y = round((mouse_y - self.offset_y) / BLOCK_SIZE)

        # Occupied cells in block's local 4×4 grid
        shape = block.get_shape()
        cells = [(k // 4, k % 4) for k in shape]

        min_j = min(j for i, j in cells)
        max_j = max(j for i, j in cells)
        min_i = min(i for i, j in cells)
        max_i = max(i for i, j in cells)

        # Shift so the cell under the mouse becomes aligned
        grid_x -= min_j
        grid_y -= min_i

        # Clamp based on ALL filled cells
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
        shape = block.get_shape()
        color = block.get_color()
        for i in range(4):
            for j in range(4):
                if i * 4 + j in shape:
                    x = screen_x + j * BLOCK_SIZE
                    y = screen_y + i * BLOCK_SIZE
                    pygame.draw.rect(
                        self.screen,
                        color,
                        [x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2]
                    )

    def _draw_dragging_block(self):
        handler = self.game_mode.input_handler
        block = handler.dragging_block

        if block:
            # Compute snapped preview position
            preview_x, preview_y = self.compute_snapped_preview(block)

            # Only draw the preview if the block isn't already fully on the board
            # Check if the current x/y matches snapped x/y
            if (block.x != preview_x) or (block.y != preview_y):
                shape = block.get_shape()
                color = block.get_color()

                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in shape:
                            pygame.draw.rect(
                                self.screen,
                                color,
                                [
                                    self.offset_x + (preview_x + j) * BLOCK_SIZE + 1,
                                    self.offset_y + (preview_y + i) * BLOCK_SIZE + 1,
                                    BLOCK_SIZE - 2,
                                    BLOCK_SIZE - 2
                                ]
                            )

    def _draw_preview(self):
        block = self.game_mode.input_handler.dragging_block
        if block:
            grid_x, grid_y = self.compute_snapped_preview(block)

            # Convert to screen coordinates
            screen_x = self.offset_x + grid_x * BLOCK_SIZE
            screen_y = self.offset_y + grid_y * BLOCK_SIZE

            # Draw the preview block
            shape = block.get_shape()
            color = block.get_color()
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in shape:
                        pygame.draw.rect(
                            self.screen,
                            color,
                            [
                                screen_x + j * BLOCK_SIZE + 1,
                                screen_y + i * BLOCK_SIZE + 1,
                                BLOCK_SIZE - 2,
                                BLOCK_SIZE - 2
                            ]
                        )

    def _draw_score(self):
        """
        Draw score and high score
        """
        score = self.state.score_manager.get_score()
        high_score = self.state.score_manager.get_highscore()
        high_score_player = self.state.score_manager.get_highscore_player()

        score_text = self.font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(score_text, [10, 10])
        high_score_text = self.font.render(f"High Score: {high_score_player} - {high_score}", True, BLACK)
        self.screen.blit(high_score_text, [10, 35])

    def _draw_game_over_message(self):
        """
        Draw "Game Over" if applicable
        """
        center_x = self.screen.get_width() // 2
        game_over_text = self.large_font.render("Game Over", True, ORANGE)
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(center_x, 160)))