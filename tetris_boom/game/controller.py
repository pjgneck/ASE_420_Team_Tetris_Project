import pygame
import game.input_overlay as Overlay
from game.modes.tetris_mode import TetrisMode
from game.modes.blockblast_mode import BlockBlastMode
from game.input_handlers.tetris_input_handler import TetrisInputHandler
from game.input_handlers.blockblast_input_handler import BlockBlastInputHandler
from game.renderers.tetris_renderer import TetrisRenderer
from game.renderers.blockblast_renderer import BlockBlastRenderer
from game.gamestate import GameState
from game.board import Board
from game.block_factory import BlockFactory
from game.sound_manager import SoundManager

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 30  # Defined FPS for clarity

class GameController:
    def __init__(self):
        """
        Initializes the game controller, setting up the screen, clock, and game mode.
        """
        # Configure the mixer
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set up the screen with given dimensions
        self.clock = pygame.time.Clock()  # Clock for controlling the frame rate
        pygame.display.set_caption("Tetris BOOM!")  # Set the window title

        self.sound_manager = SoundManager()

        board = Board()
        block_factory = BlockFactory()

        self.state = GameState(board=board, block_factory=block_factory)  # Shared game state instance

        self.last_score_checkpoint = 0

        # Initialize the game mode with required dependencies
        self.game_mode = TetrisMode(
            screen=self.screen,
            input_handler=TetrisInputHandler,
            renderer=TetrisRenderer,
            state=self.state
        )

        self.sound_manager.play("music_1")

        Overlay.get_player_name(
            screen=self.screen,
            renderer=TetrisRenderer(self.screen, self.game_mode)
        )

    def run_game_loop(self):
        is_running = True

        self.sound_manager.stop("music_1")
        self.sound_manager.play("game_start")

        while is_running:
            # Event handling
            for event in pygame.event.get():
                quit_command = self.game_mode.handle_input(event)
                if event.type == pygame.QUIT or quit_command == "quit":
                    is_running = False

            # Update the game state
            self.game_mode.update()

            # Check if score reached next multiple of 5
            current_score = self.state.score_manager.get_score()
            if current_score // 5 > self.last_score_checkpoint:
                self.last_score_checkpoint = current_score // 5
                if isinstance(self.game_mode, TetrisMode):
                    self.switch_mode(BlockBlastMode, BlockBlastInputHandler, BlockBlastRenderer)
                else:
                    self.switch_mode(TetrisMode, TetrisInputHandler, TetrisRenderer)

            # Render
            self.game_mode.render()
            self.clock.tick(FPS)

        pygame.quit()

    def switch_mode(self, new_mode_class, input_handler_class, renderer_class):
        """
        Placeholder for switching between game modes (if applicable in future).
        :param new_mode_class: The class of the mode to switch to (TetrisMode or BlockBlastMode)
        :param input_handler_class: The input handler class for the new mode
        :param renderer_class: The renderer class for the new mode
        """
        if self.state.current_block is None:
            self.state.current_block = self.state.block_factory.create_block()

        self.game_mode = new_mode_class(
            screen=self.screen,
            input_handler=input_handler_class,
            renderer=renderer_class,
            state=self.state
        )

        self.sound_manager.play("switch_modes")
