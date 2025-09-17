import pygame
from game.modes.tetris_mode import TetrisMode
from game.input_handler import TetrisInputHandler
from game.renderer import TetrisRenderer

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 400

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()

        # Create the game mode with injected dependencies
        self.mode = TetrisMode(
            screen=self.screen,
            input_handler=TetrisInputHandler,
            renderer=TetrisRenderer
        )

    def run_game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                result = self.mode.handle_input(event)
                if result == "quit":
                    running = False

            self.mode.update()
            self.mode.render()
            self.clock.tick(30)

        pygame.quit()
