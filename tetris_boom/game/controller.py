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
from game.data import NEXT_BLOCKS_COUNT

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 30
SCORE_CHECKPOINT_INTERVAL = 5


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

        self.state.next_blocks = []
        for _ in range(NEXT_BLOCKS_COUNT):
            self.state.next_blocks.append(self.block_factory.create_block())

        self.last_score_checkpoint = 0
        self.player_name ="" 

        self.dark_mode= False

    def _initialize_starting_mode(self):
        """Initialize the starting game mode using a factory method."""
        self.game_mode = self._create_mode(TetrisMode)
        pygame.mouse.set_visible(self.game_mode.should_show_cursor())
        self.sound_manager.play("music_1")
        self.dark_mode = False

    def _create_mode(self, mode_class):
        """Factory method to create any game mode with proper dependencies."""
        mode_config = {
            TetrisMode: (TetrisRenderer, TetrisInputHandler),
            BlockBlastMode: (BlockBlastRenderer, BlockBlastInputHandler)
        }
        
        renderer_class, input_handler_class = mode_config[mode_class]
        
        mode = mode_class(
            screen=self.screen,
            state=self.state,
            renderer=None
        )
        
        renderer = renderer_class(
            screen=self.screen,
            game_mode=mode
        )
        mode.renderer = renderer
        
        input_handler = input_handler_class(mode)
        mode.input_handler = input_handler
        
        return mode

    def _initialize_player(self):
        """Initialize player-specific settings."""
        self.player_name = Overlay.get_player_name(
            screen=self.screen,
            renderer=self.game_mode.renderer
        )
        from game.globals import get_player_name
        self.state.score_manager.set_player_name(get_player_name())

    def reset_game(self):
        """Reset the game to initial state."""
        self.board.grid = [[0 for _ in range(self.board.cols)] for _ in range(self.board.rows)]
        self.score_manager.reset()
        
        self.state.current_block = self.block_factory.create_block()
        self.state.next_blocks = []
        for _ in range(NEXT_BLOCKS_COUNT):
            self.state.next_blocks.append(self.block_factory.create_block())
        self.state.game_over = False
        
        self.game_mode.game_over = False
        if hasattr(self.game_mode, 'fall_timer'):
            self.game_mode.fall_timer = 0.0
        if hasattr(self.game_mode, 'pressing_down'):
            self.game_mode.pressing_down = False
        
        if hasattr(self.game_mode, 'input_handler'):
            if hasattr(self.game_mode.input_handler, 'dragging_block'):
                self.game_mode.input_handler.dragging_block = None
            if hasattr(self.game_mode.input_handler, 'preview_pos'):
                self.game_mode.input_handler.preview_pos = None
        
        self.last_score_checkpoint = 0
        
        self.sound_manager.stop("music_1_loop")
        self.sound_manager.stop("game_over")
        self.sound_manager.play("music_1_loop", loop=True)
        self.sound_manager.play("game_start")
        
        dark_mode_active = self.dark_mode
        self.switch_mode(TetrisMode, TetrisInputHandler, TetrisRenderer, dark_mode_active)

    def switch_mode(self, new_mode_class, input_handler_class, renderer_class, dark_mode):
        """
        Switch to a new game mode with specified components.
        :param new_mode_class: The class of the mode to switch to (TetrisMode or BlockBlastMode)
        :param input_handler_class: The input handler class for the new mode
        :param renderer_class: The renderer class for the new mode
        :param dark_mode: Boolean indicating if dark mode is active
        """
        if self.state.current_block is None:
            self.state.current_block = self.state.block_factory.create_block()

        mode = new_mode_class(
            screen=self.screen,
            state=self.state,
            renderer=None,
            dark_mode=dark_mode
        )

        renderer = renderer_class(
            screen=self.screen,
            game_mode = mode,
            dark_mode=dark_mode
        )

        mode.renderer = renderer

        input_handler = input_handler_class(mode)
        mode.input_handler = input_handler

        self.game_mode = mode
        
        pygame.mouse.set_visible(mode.should_show_cursor())
        
        self.sound_manager.play("switch_modes")
        from game.globals import get_player_name
        self.state.score_manager.set_player_name(get_player_name())

    def run_game_loop(self):
        """Main game loop handling input, updates, and rendering."""
        is_running = True

        self.sound_manager.stop("music_1")
        self.sound_manager.play("music_1_loop", loop=True)
        self.sound_manager.play("game_start")

        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.dark_mode = not self.dark_mode
                        self.game_mode.renderer.toggle_theme()
                
                command = self.game_mode.handle_input(event)
                if command == "quit":
                    is_running = False
                elif command == "restart":
                    self.reset_game()

            self.game_mode.update()

            current_score = self.state.score_manager.get_score()
            if current_score // SCORE_CHECKPOINT_INTERVAL > self.last_score_checkpoint:
                self.last_score_checkpoint = current_score // SCORE_CHECKPOINT_INTERVAL
                dark_mode_active = self.dark_mode
                if isinstance(self.game_mode, TetrisMode):
                    self.switch_mode(BlockBlastMode, BlockBlastInputHandler, BlockBlastRenderer, dark_mode_active)
                else:
                    self.switch_mode(TetrisMode, TetrisInputHandler, TetrisRenderer, dark_mode_active)

            self.game_mode.render()
            self.clock.tick(FPS)
            
            
        pygame.quit()
