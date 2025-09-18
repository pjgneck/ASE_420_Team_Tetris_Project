from game.block_data import WHITE, GRAY, BLACK, BLOCK_SIZE
import pygame

class TetrisRenderer:
    def __init__(self, screen, game_mode):
        """
        Initializes the TetrisRenderer class.

        :param screen: The pygame screen to render to
        :param game_mode: The current game mode that holds game state
        """
        self.screen = screen
        self.game_mode = game_mode
        self.font = pygame.font.SysFont('Calibri', 20, True, False)  # Font for small text like score
        self.large_font = pygame.font.SysFont('Calibri', 35, True, False)  # Font for large text like "Game Over"

    def render(self):
        """
        Renders the entire game scene: board, current block, score, and game over message if applicable.
        """
        self.screen.fill(WHITE)  # Fill the screen with the white background
        self._draw_game_board()  # Draw the game board with blocks
        self._draw_current_block()  # Draw the current falling block
        self._draw_score()  # Draw the current score
        if self.game_mode.game_over:
            self._draw_game_over_message()  # Draw "Game Over" message if the game is over
        pygame.display.flip()  # Update the screen to display changes

    def _draw_game_board(self):
        """
        Draws the game board, including the grid and any filled blocks.
        """
        board = self.game_mode.board
        for row in range(board.rows):
            for col in range(board.cols):
                block_value = board.grid[row][col]
                if block_value > 0:
                    pygame.draw.rect(
                        self.screen,
                        board.COLORS[block_value],  # Color based on block value
                        [col * BLOCK_SIZE + 1, row * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2]  # Position and size
                    )
                # Draw the grid outline
                pygame.draw.rect(
                    self.screen,
                    GRAY,
                    [col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE],
                    1  # 1-pixel border
                )

    def _draw_current_block(self):
        """
        Draws the current falling block at its specified position.
        """
        current_block = self.game_mode.block
        for i in range(4):  # Iterate over the 4x4 block grid
            for j in range(4):
                if i * 4 + j in current_block.get_shape():  # Check if the position is part of the current block
                    x = current_block.x + j
                    y = current_block.y + i
                    pygame.draw.rect(
                        self.screen,
                        current_block.get_color(),  # Color of the block
                        [x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2]  # Position and size
                    )

    def _draw_score(self):
        """
        Renders the current score on the screen.
        """
        score_text = self.font.render(f"Score: {self.game_mode.score_manager.get_score()}", True, BLACK)
        self.screen.blit(score_text, [5, 5])  # Position the score in the top-left corner

    def _draw_game_over_message(self):
        """
        Draws the "Game Over" message and instructions to quit.
        """
        game_over_text = self.large_font.render("Game Over", True, (255, 125, 0))  # Orange color
        press_q_text = self.large_font.render("Press Q", True, (255, 215, 0))  # Yellow color
        to_quit_text = self.large_font.render("to Quit", True, (255, 215, 0))  # Yellow color
        self.screen.blit(game_over_text, [5, 160])
        self.screen.blit(press_q_text, [30, 200])
        self.screen.blit(to_quit_text, [40, 230])
