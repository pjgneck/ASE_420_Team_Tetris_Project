import pygame
from game.block_data import WHITE, GRAY, BLACK, ORANGE, YELLOW, BLOCK_SIZE

class TetrisRenderer:
    def __init__(self, screen, game_mode):
        """
        Initializes the TetrisRenderer.

        :param screen: The pygame screen surface to render to.
        :param game_mode: The current TetrisMode instance holding game state.
        """
        self.screen = screen
        self.game_mode = game_mode

        # Fonts for rendering text
        self.font = pygame.font.SysFont('Calibri', 20, True, False)       # Score and small UI text
        self.large_font = pygame.font.SysFont('Calibri', 35, True, False) # Game over text

        # Precompute offsets to center the game board on the screen
        board = self.game_mode.board
        self.offset_x = (screen.get_width() - board.cols * BLOCK_SIZE) // 2
        self.offset_y = (screen.get_height() - board.rows * BLOCK_SIZE) // 2

    def render(self):
        """
        Renders the entire game scene — including the game board, current block,
        score display, and game-over message if applicable.
        """
        self.screen.fill(WHITE)             # Fill the background with white
        self._draw_game_board()             # Draw the board grid and frozen blocks
        self._draw_current_block()          # Draw the falling block
        self._draw_score()                  # Draw the score text

        if self.game_mode.game_over:
            self._draw_game_over_message()  # If game is over, display the end screen text

        pygame.display.flip()               # Push all drawing to the screen

    def _draw_game_board(self):
        """
        Draws the Tetris board including grid lines and any frozen (placed) blocks.
        """
        board = self.game_mode.board

        for row in range(board.rows):
            for col in range(board.cols):
                block_value = board.grid[row][col]

                # If cell contains a frozen block, draw it
                if block_value > 0:
                    pygame.draw.rect(
                        self.screen,
                        board.BLOCK_COLORS[block_value],  # Color of the block based on its ID
                        [
                            self.offset_x + col * BLOCK_SIZE + 1,
                            self.offset_y + row * BLOCK_SIZE + 1,
                            BLOCK_SIZE - 2,
                            BLOCK_SIZE - 2
                        ]
                    )

                # Draw the gray grid outline over every cell
                pygame.draw.rect(
                    self.screen,
                    GRAY,
                    [
                        self.offset_x + col * BLOCK_SIZE,
                        self.offset_y + row * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    ],
                    1  # 1-pixel border thickness
                )

    def _draw_current_block(self):
        """
        Draws the current falling block at its position on the board.
        """
        current_block = self.game_mode.block
        shape = current_block.get_shape()  # Get the list of filled cell indices (0-15)
        
        for i in range(4):  # 4x4 grid
            for j in range(4):
                # Only draw cells that are part of the shape
                if i * 4 + j in shape:
                    x = current_block.x + j
                    y = current_block.y + i

                    pygame.draw.rect(
                        self.screen,
                        current_block.get_color(),  # Color of the block
                        [
                            self.offset_x + x * BLOCK_SIZE + 1,
                            self.offset_y + y * BLOCK_SIZE + 1,
                            BLOCK_SIZE - 2,
                            BLOCK_SIZE - 2
                        ]
                    )

    def _draw_score(self):
        """
        Renders the current score in the top-left corner of the screen.
        """
        score = self.game_mode.score_manager.get_score()
        score_text = self.font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(score_text, [10, 10])  # Fixed UI position

    def _draw_game_over_message(self):
        """
        Displays a "Game Over" message and instructions to quit.
        Centered in the middle of the screen.
        """
        # Create text surfaces
        game_over_text = self.large_font.render("Game Over", True, ORANGE)
        press_q_text = self.large_font.render("Press Q", True, YELLOW)
        to_quit_text = self.large_font.render("to Quit", True, YELLOW)

        # Get center X position of screen
        center_x = self.screen.get_width() // 2

        # Center text horizontally using get_rect(center=...)
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(center_x, 160)))
        self.screen.blit(press_q_text, press_q_text.get_rect(center=(center_x, 200)))
        self.screen.blit(to_quit_text, to_quit_text.get_rect(center=(center_x, 240)))
