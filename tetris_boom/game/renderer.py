import pygame

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
BLOCK_SIZE = 20

class TetrisRenderer:
    def __init__(self, screen, game_mode):
        self.screen = screen
        self.game_mode = game_mode
        self.font = pygame.font.SysFont('Calibri', 20, True, False)
        self.big_font = pygame.font.SysFont('Calibri', 35, True, False)

    def render(self):
        self.screen.fill(WHITE)
        self.draw_board()
        self.draw_block()
        self.draw_score()
        if self.game_mode.game_over:
            self.draw_game_over()
        pygame.display.flip()

    def draw_board(self):
        board = self.game_mode.board
        for y in range(board.rows):
            for x in range(board.cols):
                val = board.grid[y][x]
                if val > 0:
                    pygame.draw.rect(
                        self.screen,
                        board.COLORS[val],
                        [x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2]
                    )
                pygame.draw.rect(
                    self.screen,
                    GRAY,
                    [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE],
                    1
                )

    def draw_block(self):
        block = self.game_mode.block
        for i in range(4):
            for j in range(4):
                if i * 4 + j in block.get_image():
                    x = block.x + j
                    y = block.y + i
                    pygame.draw.rect(
                        self.screen,
                        block.get_color(),
                        [x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2]
                    )

    def draw_score(self):
        text = self.font.render(f"Score: {self.game_mode.score_manager.get_score()}", True, BLACK)
        self.screen.blit(text, [5, 5])

    def draw_game_over(self):
        text1 = self.big_font.render("Game Over", True, (255, 125, 0))
        text2 = self.big_font.render("Press Q", True, (255, 215, 0))
        text3 = self.big_font.render("to Quit", True, (255, 215, 0))
        self.screen.blit(text1, [5, 160])
        self.screen.blit(text2, [30, 200])
        self.screen.blit(text3, [40, 230])
