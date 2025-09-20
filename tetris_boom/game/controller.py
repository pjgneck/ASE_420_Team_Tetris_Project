import pygame
from game.modes.tetris_mode import TetrisMode
from game.input_handler import TetrisInputHandler
from game.renderer import TetrisRenderer

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 30  # Defined FPS for clarity

class GameController:
    def __init__(self):
        """
        Initializes the game controller, setting up the screen, clock, and game mode.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set up the screen with given dimensions
        self.clock = pygame.time.Clock()  # Clock for controlling the frame rate
        pygame.display.set_caption("Tetris BOOM!")  # Set the window title

        # Initialize the game mode with required dependencies
        self.game_mode = TetrisMode(
            screen=self.screen,
            input_handler=TetrisInputHandler,
            renderer=TetrisRenderer
        )


    def run_game_loop(self):
        """
        Runs the main game loop, handling events, updating the game state, and rendering.
        """
        is_running = True

        while is_running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False  # Exit the game loop
                else:
                    quit_command = self.game_mode.handle_input(event)
                    if quit_command == "quit":
                        is_running = False  # Exit if the game mode signals to quit

            # Update the game state and render the scene
            self.game_mode.update()
            self.game_mode.render()

            # Control the frame rate
            self.clock.tick(FPS)

        pygame.quit()  # Cleanly quit pygame when the game loop ends

    def switch_mode(self):
        """
        Placeholder for switching between game modes (if applicable in future).
        """
        pass
