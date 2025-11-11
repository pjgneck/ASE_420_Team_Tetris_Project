import pygame
from game.modes.base_mode import GameMode
from game.gamestate import GameState
from game.renderers.base_renderer import BaseRenderer

class BlockBlastMode(GameMode):
    def __init__(self, screen: pygame.Surface, state: GameState, renderer: BaseRenderer):
        """
        :param state: Shared GameState instance containing board, score, etc.
        """
        self.screen = screen
        self.state = state  # Shared game state
        self.renderer = renderer
        self.input_handler = None # Will be injected after creation
        self.game_over = False

        if not self.state.next_blocks:
            for _ in range(3):
                self.state.next_blocks.append(self.state.block_factory.create_block())

    def update(self):
        """
        Update game logic.
        For BlockBlast, blocks don't fall automatically. Only handle dragging.
        """
        has_space = any(
            self.state.board.has_space_for_block(block.copy())
            for block in self.state.next_blocks
        )

        # Check game over
        if not has_space:
            self._handle_game_over()

    def handle_input(self, event):
        """
        Handle input events (mouse drag-and-drop for blocks).
        """
        # Pass event to input handler
        return self.input_handler.handle(event)

    def render(self):
        """
        Render the game state on the screen.
        """
        self.renderer.render()

    def spawn_block(self):
        pass  # No falling block in BlockBlast
