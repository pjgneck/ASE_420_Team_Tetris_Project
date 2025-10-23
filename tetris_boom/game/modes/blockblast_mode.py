import pygame
from game.modes.base_mode import GameMode

class BlockBlastMode(GameMode):
    def __init__(self, screen, input_handler, renderer, state):
        """
        :param state: Shared GameState instance containing board, score, etc.
        """
        self.state = state
        self.input_handler = input_handler(self)
        self.renderer = renderer(screen, self)
        self.screen = screen
        self.game_over = False

        if not self.state.next_blocks:
            for _ in range(3):
                self.state.next_blocks.append(self.state.block_factory.create_block())
        # BlockBlast-specific attributes
        self.next_pieces = [self.state.block_factory.create_block() for _ in range(3)]
        self.dragging_piece = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def update(self):
        """
        Update game logic.
        For BlockBlast, blocks don't fall automatically. Only handle dragging.
        """
        self.game_over = not any(
            self.state.board.has_space_for_block(block.copy())
            for block in self.state.next_blocks
        )

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
        self.renderer.render()  # Render the shared board
        self._draw_next_pieces()  # Render BlockBlast-specific pieces

    def _draw_next_pieces(self):
        """
        Draw the next 3 pieces available for drag-and-drop.
        """
        for idx, piece in enumerate(self.next_pieces):
            if piece == self.dragging_piece:
                # Skip drawing while dragging (it follows the mouse)
                continue

            # Example placement: top-right corner
            piece_screen_x = self.screen.get_width() - 100
            piece_screen_y = 50 + idx * 70
            self.renderer.draw_block_at_screen_coords(piece, piece_screen_x, piece_screen_y)

        # Draw dragging piece following the mouse
        if self.dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.renderer.draw_block_at_screen_coords(
                self.dragging_piece,
                mouse_x - self.drag_offset_x,
                mouse_y - self.drag_offset_y
            )

    def spawn_block(self):
        pass  # No falling block in BlockBlast
