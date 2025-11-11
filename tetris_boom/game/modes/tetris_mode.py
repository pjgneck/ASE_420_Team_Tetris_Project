import pygame
from game.modes.base_mode import GameMode

class TetrisMode(GameMode):
    def __init__(self, screen: pygame.Surface, input_handler, renderer, state, dark_mode=False):
        """
        :param state: Shared GameState instance containing board, score, block pool, etc.
        """
        self.state = state  # Shared game state
        self.input_handler = input_handler(self)
        self.renderer = renderer(screen, self, dark_mode=dark_mode)
        self.screen = screen
        self.game_over = False
        self.gravity = 1.5
        self.fall_timer = 0.0
        self.pressing_down = False

    def update(self):
        if self.game_over:
            return

        dt = 1 / 30  # time per frame
        self.fall_timer += dt

        # Drop faster if "down" is pressed
        speed_multiplier = 5 if getattr(self, "pressing_down", False) else 1
        drop_interval = 1.0 / (self.gravity * speed_multiplier)

        if self.fall_timer >= drop_interval:
            self.fall_timer = 0.0

            # Move block down
            self.state.current_block.move(0, 1)

            # If block is now in an invalid position, revert and lock
            if not self.state.board.is_valid_position(self.state.current_block):
                self.state.current_block.move(0, -1)  # back to last valid spot
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

        # Clear lines & update score
        lines_cleared = self.state.board.break_lines()
        self.state.score_manager.add_points(lines_cleared)

        # Spawn new block
        self.spawn_block()

        # Check game over
        if not self.state.board.is_valid_position(self.state.current_block):
            self.game_over = True

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
