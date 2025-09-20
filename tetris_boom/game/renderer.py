import pygame
from game.block_data import WHITE, GRAY, BLACK, ORANGE, YELLOW, BLOCK_SIZE
from game.score_manager import ScoreManager

import pygame

def get_player_name(screen, renderer):
    """
    Displays an input overlay for entering the player's name,
    while showing the game board in the background.
    """
    font = pygame.font.SysFont("Calibri", 30, True)
    small_font = pygame.font.SysFont("Calibri", 20, False)

    input_box = pygame.Rect(screen.get_width()//2 - 150, screen.get_height()//2, 300, 50)
    color_active = pygame.Color("dodgerblue2")
    color_inactive = pygame.Color("gray60")
    color = color_inactive
    active = True
    text = ""
    cursor_visible = True
    cursor_timer = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Player"
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text.strip() if text.strip() != "" else "Player"
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 15:  # limit name length
                            text += event.unicode

        # Draw the game board in the background
        screen.fill((255, 255, 255))
        renderer._draw_game_board()

        # Draw translucent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))  # white with 70% opacity
        screen.blit(overlay, (0, 0))

        # Draw prompt
        prompt = font.render("Enter your name:", True, (0, 0, 0))
        screen.blit(prompt, (screen.get_width()//2 - prompt.get_width()//2, screen.get_height()//2 - 80))

        # Draw input text with cursor
        cursor_timer += 1
        if cursor_timer >= 30:  # blink every 0.5 sec
            cursor_visible = not cursor_visible
            cursor_timer = 0

        display_text = text
        if cursor_visible:
            display_text += "|"

        txt_surface = font.render(display_text, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x+10, input_box.y+10))

        # Draw input box
        pygame.draw.rect(screen, color, input_box, 2)

        # Instruction
        info_text = small_font.render("Press Enter to confirm", True, (50, 50, 50))
        screen.blit(info_text, (screen.get_width()//2 - info_text.get_width()//2, input_box.y + 60))

        pygame.display.flip()
        clock.tick(30)


class TetrisRenderer:
    def __init__(self, screen, game_mode):
        self.screen = screen
        self.game_mode = game_mode

        # Precompute offsets first
        board = self.game_mode.board
        self.offset_x = (screen.get_width() - board.cols * BLOCK_SIZE) // 2
        self.offset_y = (screen.get_height() - board.rows * BLOCK_SIZE) // 2

        # Now ask for player name
        self.player_name = get_player_name(screen, self)
        self.game_mode.score_manager.player_name = self.player_name

        # Fonts
        self.font = pygame.font.SysFont('Calibri', 20, True, False)
        self.large_font = pygame.font.SysFont('Calibri', 35, True, False)

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
        Renders the current score and high score in the top-left corner of the screen.
        """
        score = self.game_mode.score_manager.get_score()
        high_score = self.game_mode.score_manager.get_highscore() 
        high_score_player = self.game_mode.score_manager.get_highscore_player() 

        # Current score
        score_text = self.font.render(f"Score: {score}", True, BLACK)
        self.screen.blit(score_text, [10, 10])

        # High score (drawn just below the current score)
        high_score_text = self.font.render(f"High Score: {high_score_player} - {high_score}", True, BLACK)
        self.screen.blit(high_score_text, [10, 35])


    def _draw_game_over_message(self):
        """
        Displays a "Game Over" message.
        If the player achieved a new high score, congratulate them.
        """
        center_x = self.screen.get_width() // 2

        # Always show "Game Over"
        game_over_text = self.large_font.render("Game Over", True, ORANGE)
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(center_x, 160)))

        # Get current score and highscore info
        score_manager = self.game_mode.score_manager
        current_score = score_manager.get_score()
        highscore_name = score_manager.get_highscore_player()
        highscore = score_manager.get_highscore()

        # If the player set the high score, show a congratulatory message
        if score_manager.player_name == highscore_name and current_score == highscore:
            congrats_text = self.font.render(
                f"Congrats {score_manager.player_name}!", True, YELLOW
            )
            points_text = self.font.render(
                f"New High Score: {current_score} points!", True, YELLOW
            )
            self.screen.blit(congrats_text, congrats_text.get_rect(center=(center_x, 210)))
            self.screen.blit(points_text, points_text.get_rect(center=(center_x, 240)))
        else:
            # Otherwise, just show standard "Press Q to Quit"
            press_q_text = self.large_font.render("Press Q", True, YELLOW)
            to_quit_text = self.large_font.render("to Quit", True, YELLOW)
            self.screen.blit(press_q_text, press_q_text.get_rect(center=(center_x, 200)))
            self.screen.blit(to_quit_text, to_quit_text.get_rect(center=(center_x, 240)))
        
