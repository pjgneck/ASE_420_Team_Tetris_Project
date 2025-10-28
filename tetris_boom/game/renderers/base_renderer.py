import pygame

from game.data import BLACK, BLOCK_SIZE, GRAY, ORANGE, YELLOW, LIGHT_THEME, DARK_THEME, DARK_BLOCK_COLORS, DARK_BLOCK_OUTLINE, LIGHT_BLOCK_COLORS, LIGHT_BLOCK_OUTLINE

class BaseRenderer:
    def __init__(self, screen, game_mode, dark_mode=False):
        self.screen = screen
        self.game_mode = game_mode
        self.state = game_mode.state
        self.board = self.state.board

        self.offset_x = (screen.get_width() - self.board.cols * BLOCK_SIZE) // 2
        self.offset_y = (screen.get_height() - self.board.rows * BLOCK_SIZE) // 2

        self.font = pygame.font.SysFont('Calibri', 20, True)
        self.large_font = pygame.font.SysFont('Calibri', 35, True)

        self.dark_mode = dark_mode
        self.theme = DARK_THEME if dark_mode else LIGHT_THEME

    def toggle_theme(self):
        """
        Switch between dark and light modes.
        """
        self.dark_mode = not self.dark_mode
        self.theme = DARK_THEME if self.dark_mode else LIGHT_THEME

    def _draw_background(self):
        """
        Fill screen with background color
        """
        self.screen.fill(self.theme["background"])

    def _draw_game_board(self):
        """
        Draws the board grid and frozen blocks (no falling block)
        """
        board = self.state.board
        colors = DARK_BLOCK_COLORS if self.dark_mode else LIGHT_BLOCK_COLORS
        outline_color = DARK_BLOCK_OUTLINE if self.dark_mode else LIGHT_BLOCK_OUTLINE
        for row in range(board.rows):
            for col in range(board.cols):
                block_value = board.grid[row][col]
                if block_value > 0:
                    pygame.draw.rect(
                        self.screen,
                        colors[block_value],
                        [
                            self.offset_x + col * BLOCK_SIZE + 1,
                            self.offset_y + row * BLOCK_SIZE + 1,
                            BLOCK_SIZE - 2,
                            BLOCK_SIZE - 2
                        ]
                    )
                    pygame.draw.rect(
                        self.screen,
                        outline_color,
                        [
                            self.offset_x + col * BLOCK_SIZE,
                            self.offset_y + row * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE
                        ],
                        1
                    )
                # Draw grid
                pygame.draw.rect(
                    self.screen,
                    self.theme["grid"],
                    [
                        self.offset_x + col * BLOCK_SIZE,
                        self.offset_y + row * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    ],
                    1
                )
    
    def _draw_score(self):
        """
        Draw score and high score
        """
        score_manager = self.state.score_manager
        score = score_manager.get_score()
        high_score = score_manager.get_highscore()
        high_score_player = score_manager.get_highscore_player()

        score_text = self.font.render(f"Score: {score}", True, self.theme["text"])
        self.screen.blit(score_text, [10, 10])

        high_score_text = self.font.render(f"High Score: {high_score_player} - {high_score}", True, self.theme["text"])
        self.screen.blit(high_score_text, [10, 35])

    def _draw_game_over_message(self):
        """
        Draw "Game Over" message
        """
        center_x = self.screen.get_width() // 2
        score_manager = self.state.score_manager
        current_score = score_manager.get_score()
        highscore = score_manager.get_highscore()
        highscore_name = score_manager.get_highscore_player()

        game_over_text = self.large_font.render("Game Over", True, self.theme["game_over"])
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(center_x, 160)))

        if score_manager.player_name == highscore_name and current_score == highscore:
            congrats_text = self.font.render(f"Congrats {score_manager.player_name}!", True, self.theme["highlight"])
            points_text = self.font.render(f"New High Score: {current_score} points!", True, self.theme["highlight"])
            self.screen.blit(congrats_text, congrats_text.get_rect(center=(center_x, 210)))
            self.screen.blit(points_text, points_text.get_rect(center=(center_x, 240)))
        else:
            press_q_text = self.large_font.render("Press Q", True, self.theme["highlight"])
            to_quit_text = self.large_font.render("to Quit", True, self.theme["highlight"])
            self.screen.blit(press_q_text, press_q_text.get_rect(center=(center_x, 200)))
            self.screen.blit(to_quit_text, to_quit_text.get_rect(center=(center_x, 240)))
