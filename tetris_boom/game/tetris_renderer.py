import pygame
from game.globals import get_player_name
from game.block_data import WHITE, GRAY, BLACK, ORANGE, YELLOW, BLOCK_SIZE

class TetrisRenderer:
    def __init__(self, screen, game_mode):
        self.screen = screen
        self.game_mode = game_mode
        self.state = self.game_mode.state  # Shared GameState

        # Precompute offsets
        board = self.state.board
        self.offset_x = (screen.get_width() - board.cols * BLOCK_SIZE) // 2
        self.offset_y = (screen.get_height() - board.rows * BLOCK_SIZE) // 2

        # Set player name
        self.player_name = get_player_name()
        self.state.score_manager.player_name = self.player_name

        # Fonts
        self.font = pygame.font.SysFont('Calibri', 20, True, False)
        self.large_font = pygame.font.SysFont('Calibri', 35, True, False)

    def render(self):
        self.screen.fill(WHITE)
        self._draw_game_board()
        self._draw_current_block()
        self._draw_score()

        if self.game_mode.game_over:
            self._draw_game_over_message()

        pygame.display.flip()

    def _draw_game_board(self):
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

    def _draw_score(self):
        score_manager = self.state.score_manager
        score = score_manager.get_score()
        high_score = score_manager.get_highscore()
        high_score_player = score_manager.get_highscore_player()

        score_text = self.font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(score_text, [10, 10])

        high_score_text = self.font.render(f"High Score: {high_score_player} - {high_score}", True, BLACK)
        self.screen.blit(high_score_text, [10, 35])

    def _draw_game_over_message(self):
        center_x = self.screen.get_width() // 2
        score_manager = self.state.score_manager
        current_score = score_manager.get_score()
        highscore = score_manager.get_highscore()
        highscore_name = score_manager.get_highscore_player()

        game_over_text = self.large_font.render("Game Over", True, ORANGE)
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(center_x, 160)))

        if score_manager.player_name == highscore_name and current_score == highscore:
            congrats_text = self.font.render(f"Congrats {score_manager.player_name}!", True, YELLOW)
            points_text = self.font.render(f"New High Score: {current_score} points!", True, YELLOW)
            self.screen.blit(congrats_text, congrats_text.get_rect(center=(center_x, 210)))
            self.screen.blit(points_text, points_text.get_rect(center=(center_x, 240)))
        else:
            press_q_text = self.large_font.render("Press Q", True, YELLOW)
            to_quit_text = self.large_font.render("to Quit", True, YELLOW)
            self.screen.blit(press_q_text, press_q_text.get_rect(center=(center_x, 200)))
            self.screen.blit(to_quit_text, to_quit_text.get_rect(center=(center_x, 240)))
