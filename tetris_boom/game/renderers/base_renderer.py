import pygame

from game.data import *
from game.modes.base_mode import GameMode

class BaseRenderer:
    def __init__(self, screen: pygame.Surface, game_mode: GameMode, dark_mode=False):
        self.screen = screen
        self.game_mode = game_mode
        self.dark_mode = False
        self.state = game_mode.state
        self.board = self.state.board

        self.offset_x = (screen.get_width() - self.board.cols * BLOCK_SIZE) // 2
        SCORE_AREA_HEIGHT = 70
        self.offset_y = SCORE_AREA_HEIGHT + (screen.get_height() - SCORE_AREA_HEIGHT - self.board.rows * BLOCK_SIZE) // 2

        self.font = pygame.font.SysFont('Calibri', 20, True)
        self.large_font = pygame.font.SysFont('Calibri', 35, True)

        self.dark_mode = dark_mode
        self.theme = DARK_THEME if dark_mode else LIGHT_THEME

        self.sound_manager = self.state.sound_manager
        self._load_theme()

    def _load_theme(self):
        """Load color them based on settings"""
        if self.dark_mode:
            self.theme = DARK_THEME
        else:
            self.theme = LIGHT_THEME

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self._load_theme()

    def set_theme(self, dark_mode: bool):
        self.dark_mode = dark_mode
        self._load_theme()
    
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
        self.state.score_manager.update_leaderboard()

        center_x = self.screen.get_width() // 2
        score_manager = self.state.score_manager
        player_name = score_manager.player_name
        current_score = score_manager.get_score()
        highscore = score_manager.get_highscore()
        highscore_name = score_manager.get_highscore_player()

        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((128, 128, 128, 200))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.large_font.render("Game Over", True, self.theme["game_over"])
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(center_x, 160)))

        if score_manager.player_name == highscore_name and current_score == highscore and current_score > 0:
            congrats_text = self.font.render(f"Congrats {score_manager.player_name}!", True, self.theme["highlight"])
            points_text = self.font.render(f"New High Score: {current_score} points!", True, self.theme["highlight"])
            self.screen.blit(congrats_text, congrats_text.get_rect(center=(center_x, 210)))
            self.screen.blit(points_text, points_text.get_rect(center=(center_x, 240)))
            quit_y = 275
            restart_y = 300
            leaderboard_start_y = 330
        else:
            quit_y = 200
            restart_y = 225
            leaderboard_start_y = 280
        
        quit_text = self.font.render("Press Q to quit", True, self.theme["highlight"])
        restart_text = self.font.render("Press R to restart", True, self.theme["highlight"])
        self.screen.blit(quit_text, quit_text.get_rect(center=(center_x, quit_y)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(center_x, restart_y)))

        leaderboard_header = self.font.render("Leaderboard:", True, BLACK)
        self.screen.blit(leaderboard_header, leaderboard_header.get_rect(center=(center_x, leaderboard_start_y)))

        for i, entry in enumerate(score_manager.get_leaderboard(), start=1):
            if entry['name'] == player_name and entry['score'] == current_score:
                color = ORANGE
            else:
                color = BLACK

            entry_text = self.font.render(f"{i}. {entry['name']} - {entry['score']}", True, color)
            self.screen.blit(entry_text, entry_text.get_rect(center=(center_x, leaderboard_start_y + 25 * i)))
