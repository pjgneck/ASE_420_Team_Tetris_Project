import pygame
from game.modes.tetris_mode import TetrisMode
from game.modes.blockblast_mode import BlockBlastMode
from game.input_handler import TetrisInputHandler, BlockBlastInputHandler
from game.renderer import TetrisRenderer, BlockBlastRenderer
from game.gamestate import GameState
from game.board import Board
from game.block_factory import BlockFactory

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

        board = Board()
        block_factory = BlockFactory()

        self.state = GameState(board=board, block_factory=block_factory)  # Shared game state instance

        # Initialize the game mode with required dependencies
        self.game_mode = TetrisMode(
            screen=self.screen,
            input_handler=TetrisInputHandler,
            renderer=TetrisRenderer,
            state=self.state
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        if isinstance(self.game_mode, TetrisMode):
                            self.switch_mode(BlockBlastMode, BlockBlastInputHandler, BlockBlastRenderer)
                        else:
                            self.switch_mode(TetrisMode, TetrisInputHandler, TetrisRenderer)
                        continue
                
                quit_command = self.game_mode.handle_input(event)
                if quit_command == "quit":
                    is_running = False  # Exit if the game mode signals to quit

            # Update the game state and render the scene
            self.game_mode.update()
            self.game_mode.render()

            # Control the frame rate
            self.clock.tick(FPS)

        pygame.quit()  # Cleanly quit pygame when the game loop ends

    def switch_mode(self, new_mode_class, input_handler_class, renderer_class):
        """
        Placeholder for switching between game modes (if applicable in future).
        :param new_mode_class: The class of the mode to switch to (TetrisMode or BlockBlastMode)
        :param input_handler_class: The input handler class for the new mode
        :param renderer_class: The renderer class for the new mode
        """
        self.state.current_block = None

        self.game_mode = new_mode_class(
            screen=self.screen,
            input_handler=input_handler_class,
            renderer=renderer_class,
            state=self.state
        )
