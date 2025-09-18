import pygame
from game.board import Board
from game.block_factory import BlockFactory
from game.score_manager import ScoreManager
from game.modes.base import GameMode

class TetrisMode(GameMode):
    def __init__(self, screen: pygame.Surface, input_handler, renderer):
        """
        Initializes the Tetris game mode with the necessary components.
        
        :param screen: The pygame surface to render the game.
        :param input_handler: The input handler instance for managing player input.
        :param renderer: The renderer class responsible for drawing the game.
        """
        # Initialize game components
        self.factory = BlockFactory()  # Factory for creating new Tetriminos
        self.block = self.factory.create_block()  # Initial block
        self.board = Board()  # The game board (where blocks land)
        self.score_manager = ScoreManager()  # Manages the score
        self.input_handler = input_handler(self)  # Handles user input
        self.renderer = renderer(screen, self)  # Renders the game state
        self.screen = screen  # The screen to render to
        self.game_over = False  # Flag indicating whether the game is over
        self.gravity = 1.5  # The gravity value controls block fall speed
        self.fall_timer = 0.0  # Timer to control block falling
        self.pressing_down = False  # Flag to check if down key is being pressed for fast dropping

    def update(self):
        """
        Updates the game state. Handles block falling, collision, line clearing, and game over logic.
        """
        if self.game_over:
            return

        # Time-based falling: calculate how much time has passed (assuming 30 FPS)
        dt = 1 / 30  # Time delta (seconds per frame)
        self.fall_timer += dt

        # Calculate the drop interval based on gravity
        drop_interval = 1.0 / self.gravity

        if self.fall_timer >= drop_interval or self.pressing_down:
            self._drop_block()  # Move the block down

            # Check if the block is in a valid position
            if not self.board.is_valid_position(self.block):
                self._lock_block()  # Lock the block in place

            self.fall_timer = 0.0  # Reset fall timer after move

    def _drop_block(self):
        """
        Moves the block down and checks for collision.
        """
        self.block.move(0, 1)

    def _lock_block(self):
        """
        Locks the block in place and clears any full lines.
        """
        # Revert block position and freeze it
        self.block.move(0, -1)
        self.board.freeze(self.block)

        # Clear lines and update the score
        lines_cleared = self.board.break_lines()
        self.score_manager.add_points(lines_cleared)

        # Create a new block
        self.spawn_block()

        # Check if the game is over (can't spawn new block)
        if not self.board.is_valid_position(self.block):
            self.game_over = True

    def handle_input(self, event: pygame.event.Event) -> str:
        """
        Handles player input events (key presses).

        :param event: The input event from pygame.
        :return: The result of the input handler's processing.
        """
        return self.input_handler.handle(event)

    def render(self):
        """
        Renders the game state on the screen.
        """
        self.renderer.render()

    def spawn_block(self):
        """
        Spawns a new block by creating it via the factory.
        """
        self.block = self.factory.create_block()
