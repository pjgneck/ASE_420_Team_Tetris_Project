import pygame
from game.modes.base_mode import GameMode
from game.renderers.base_renderer import BaseRenderer
from game.gamestate import GameState

DEFAULT_GRAVITY = 1.5
SOFT_DROP_SPEED_MULTIPLIER = 5
FPS = 30

class TetrisMode(GameMode):
    def __init__(self, screen: pygame.Surface, state: GameState, renderer: BaseRenderer, dark_mode=False):
        """
        :param state: Shared GameState instance containing board, score, block pool, etc.
        """
        self.screen = screen
        self.state = state
        self.renderer = renderer
        self.input_handler = None
        self.game_over = False
        self.gravity = DEFAULT_GRAVITY
        self.fall_timer = 0.0
        self.pressing_down = False

    def update(self):
        if self.game_over:
            return

        dt = 1 / FPS
        self.fall_timer += dt

        speed_multiplier = SOFT_DROP_SPEED_MULTIPLIER if getattr(self, "pressing_down", False) else 1
        drop_interval = 1.0 / (self.gravity * speed_multiplier)

        if self.fall_timer >= drop_interval:
            self.fall_timer = 0.0

            self.state.current_block.move(0, 1)

            if not self.state.board.is_valid_position(self.state.current_block):
                self.state.current_block.move(0, -1)
                self._lock_block()

    def _drop_block(self):
        """
        Moves the block down and checks for collision.
        """
        self.state.current_block.move(0, 1)

    def _lock_block(self):
        """
        Locks the block in place and clears any full lines.
        """
        self.state.board.freeze(self.state.current_block)

        lines_cleared = self.state.board.break_lines()
        self.state.score_manager.add_points(lines_cleared)

        self.spawn_block()

        if not self.state.board.is_valid_position(self.state.current_block):
            self._handle_game_over()


    def handle_input(self, event):
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
        self.state.current_block = self.state.block_factory.create_block()

    def should_show_cursor(self) -> bool:
        return False
