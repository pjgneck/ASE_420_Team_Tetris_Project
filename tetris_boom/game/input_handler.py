import pygame

class TetrisInputHandler:
    def __init__(self, game_mode):
        """
        Initializes the input handler for the game.

        :param game_mode: The game mode instance containing the game state
        """
        self.game_mode = game_mode

    def handle(self, event):
        """
        Handles key events for player input (move, rotate, drop, etc.).

        :param event: The pygame event that is processed
        """
        current_block = self.game_mode.block  # The current falling block
        game_board = self.game_mode.board  # The game board
        block_factory = self.game_mode.factory  # Block factory to create new blocks

        if event.type == pygame.KEYDOWN:
            if self.game_mode.game_over and event.key == pygame.K_q:
                return "quit"  # Quit the game if game over and 'Q' is pressed

            # Handle left movement
            if event.key == pygame.K_LEFT:
                current_block.move(-1, 0)
                if not game_board.is_valid_position(current_block):
                    current_block.move(1, 0)  # Undo move if invalid position

            # Handle right movement
            elif event.key == pygame.K_RIGHT:
                current_block.move(1, 0)
                if not game_board.is_valid_position(current_block):
                    current_block.move(-1, 0)  # Undo move if invalid position

            # Handle down movement (start fast dropping)
            elif event.key == pygame.K_DOWN:
                self.game_mode.pressing_down = True

            # Handle rotation
            elif event.key == pygame.K_UP:
                current_block.rotate()
                if not game_board.is_valid_position(current_block):
                    current_block.undo_rotate()  # Undo rotation if invalid position

            # Handle hard drop (immediately place the block at the lowest valid position)
            elif event.key == pygame.K_SPACE:
                while game_board.is_valid_position(current_block):
                    current_block.move(0, 1)  # Move block down until it can't move
                current_block.move(0, -1)  # Undo the last move
                game_board.freeze(current_block)  # Freeze the block in place

                lines_cleared = game_board.break_lines()  # Clear full lines
                self.game_mode.score_manager.add_points(lines_cleared)  # Update score based on lines cleared
                self.game_mode.block = block_factory.create_block()  # Create a new block

                # If the new block can't be placed, the game is over
                if not game_board.is_valid_position(self.game_mode.block):
                    self.game_mode.game_over = True

        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            self.game_mode.pressing_down = False  # Stop fast dropping when the down key is released
