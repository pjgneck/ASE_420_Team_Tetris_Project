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
from game.score_manager import ScoreManager

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 30


class GameController:
    """
    Manages the main game loop, initialization of core components, 
    switching between game modes, handling player input, and rendering.
    Responsible for setting up pygame, sound, score, board, block factory, 
    game state, and managing transitions between Tetris and BlockBlast modes.
    """

    def __init__(self):
        self._initialize_pygame()
        self._initialize_core_components()
        self._initialize_starting_mode()
        self._initialize_player()

    def _initialize_pygame(self):
        """Initialize pygame and display settings."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris BOOM!")

    def _initialize_core_components(self):
        """Initialize all core game components."""
        self.sound_manager = SoundManager()
        self.score_manager = ScoreManager(sound_manager=self.sound_manager)
        self.board = Board()
        self.block_factory = BlockFactory()

        self.state = GameState(
            board=self.board,
            block_factory=self.block_factory,
            score_manager=self.score_manager,
            sound_manager=self.sound_manager
        )

        # Initialize next_blocks for BlockBlast mode
        self.state.next_blocks = []
        for _ in range(3):
            self.state.next_blocks.append(self.block_factory.create_block())

        self.last_score_checkpoint = 0

    def _initialize_starting_mode(self):
        """Initialize the starting game mode using a factory method."""
        self.game_mode = self._create_mode(TetrisMode)
        self.sound_manager.play("music_1")

    def _create_mode(self, mode_class):
        """Factory method to create any game mode with proper dependencies."""
        # Create renderer first, then mode, then input handler
        if mode_class == TetrisMode:
            mode = TetrisMode(
                screen=self.screen, 
                state=self.state,
                renderer=None  # Will set after creation
            )
            renderer = TetrisRenderer(
                screen=self.screen, 
                game_mode=mode
            )
            mode.renderer = renderer
            input_handler = TetrisInputHandler(mode)
        
        else:  # BlockBlastMode
            mode = BlockBlastMode(
                screen=self.screen, 
                state=self.state, 
                renderer=None  # Will set after creation
            )
            renderer = BlockBlastRenderer(
                screen=self.screen, 
                game_mode=mode
            )
            mode.renderer = renderer
            input_handler = BlockBlastInputHandler(mode)

        mode.input_handler = input_handler
        return mode

    def _initialize_player(self):
        """Initialize player-specific settings."""
        Overlay.get_player_name(
            screen=self.screen,
            renderer=self.game_mode.renderer
        )
        # Set the player name in the score manager
        from game.globals import get_player_name
        self.state.score_manager.set_player_name(get_player_name())

    def switch_mode(self, new_mode_class):
        """Switch to a new game mode using the factory."""
        if self.state.current_block is None:
            self.state.current_block = self.state.block_factory.create_block()

        self.game_mode = self._create_mode(new_mode_class)
        self.sound_manager.play("switch_modes")

    def run_game_loop(self):
        """Main game loop handling input, updates, and rendering."""
        is_running = True

        self.sound_manager.stop("music_1")
        self.sound_manager.play("music_1_loop", loop=True)
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
                    self.switch_mode(BlockBlastMode)
                else:
                    self.switch_mode(TetrisMode)

            # Render
            self.game_mode.render()
            self.clock.tick(FPS)

        pygame.quit()