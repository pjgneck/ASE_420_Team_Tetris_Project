import pygame

class TetrisInputHandler:
    def __init__(self, tetris_mode):
        """
        Input handler for TetrisMode.

        :param tetris_mode: The TetrisMode instance (needed for pressing_down and game_over)
        """
        self.tetris_mode = tetris_mode  # Reference to the mode
        self.state = tetris_mode.state   # Reference to shared game state

    def handle(self, event):
        """
        Handles key events: move, rotate, soft/hard drop, quit.
        """
        current_block = self.state.current_block
        board = self.state.board
        factory = self.state.block_factory

        if event.type == pygame.KEYDOWN:
            # Quit game if game over and Q is pressed
            if self.tetris_mode.game_over and event.key == pygame.K_q:
                return "quit"

            # Left
            if event.key == pygame.K_LEFT:
                current_block.move(-1, 0)
                if not board.is_valid_position(current_block):
                    current_block.move(1, 0)

            # Right
            elif event.key == pygame.K_RIGHT:
                current_block.move(1, 0)
                if not board.is_valid_position(current_block):
                    current_block.move(-1, 0)

            # Start soft drop
            elif event.key == pygame.K_DOWN:
                self.tetris_mode.pressing_down = True

            # Rotate
            elif event.key == pygame.K_UP:
                current_block.rotate()
                if not board.is_valid_position(current_block):
                    current_block.undo_rotate()

            # Hard drop
            elif event.key == pygame.K_SPACE:
                while board.is_valid_position(current_block):
                    current_block.move(0, 1)
                current_block.move(0, -1)
                board.freeze(current_block)

                # Clear lines and update score
                lines_cleared = board.break_lines()
                self.state.score_manager.add_points(lines_cleared)

                # Spawn new block
                self.state.current_block = factory.create_block()

                # Check for game over
                if not board.is_valid_position(self.state.current_block):
                    self.tetris_mode.game_over = True

        elif event.type == pygame.KEYUP:
            # Stop soft drop
            if event.key == pygame.K_DOWN:
                self.tetris_mode.pressing_down = False
