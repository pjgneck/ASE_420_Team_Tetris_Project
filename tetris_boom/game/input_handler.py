import pygame
from game.block_data import BLOCK_SIZE

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

class BlockBlastInputHandler:
    def __init__(self, blockblast_mode):
        """
        Input handler for BlockBlastMode.
        Drag-and-drop blocks onto the board.
        """
        self.blockblast_mode = blockblast_mode
        self.state = blockblast_mode.state
        self.dragging_block = None
        self.drag_offset = (0, 0)
        self.original_pos = (0, 0)

    def handle(self, event):
        board = self.state.board
        renderer = self.blockblast_mode.renderer

        # Mouse down: start dragging a next piece
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for idx, block in enumerate(self.state.next_blocks[:3]):
                    start_x = renderer.offset_x + board.cols * BLOCK_SIZE + 50
                    start_y = renderer.offset_y + idx * 100

                    shape = block.get_shape()
                    cells = [(k // 4, k % 4) for k in shape]

                    # Determine top-left of shape in screen coordinates
                    min_i = min(i for i, j in cells)
                    min_j = min(j for i, j in cells)
                    max_i = max(i for i, j in cells)
                    max_j = max(j for i, j in cells)

                    block_rect = pygame.Rect(
                        start_x + min_j * BLOCK_SIZE,
                        start_y + min_i * BLOCK_SIZE,
                        (max_j - min_j + 1) * BLOCK_SIZE,
                        (max_i - min_i + 1) * BLOCK_SIZE
                    )

                    if block_rect.collidepoint(event.pos):
                        self.dragging_block = block
                        # Offset from mouse to block top-left
                        self.drag_offset = (block_rect.x - event.pos[0], block_rect.y - event.pos[1])
                        self.original_pos = (block.x, block.y)
                        block.screen_x = event.pos[0] - self.drag_offset[0]
                        block.screen_y = event.pos[1] - self.drag_offset[1]
                        break

        # Mouse motion: move the block if dragging
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_block:
                self.dragging_block.screen_x = event.pos[0] + self.drag_offset[0]
                self.dragging_block.screen_y = event.pos[1] + self.drag_offset[1]

        # Mouse up: try to place the block on the board
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_block:
                shape = self.dragging_block.get_shape()
                cells = [(k // 4, k % 4) for k in shape]
                min_i = min(i for i, j in cells)
                min_j = min(j for i, j in cells)

                # Convert screen position to board coordinates, subtract shape offset
                grid_x = (self.dragging_block.screen_x - renderer.offset_x) // BLOCK_SIZE - min_j
                grid_y = (self.dragging_block.screen_y - renderer.offset_y) // BLOCK_SIZE - min_i

                self.dragging_block.x = grid_x
                self.dragging_block.y = grid_y

                if board.is_valid_position(self.dragging_block):
                    board.freeze(self.dragging_block)
                    lines_cleared = board.break_lines()
                    self.state.score_manager.add_points(lines_cleared)

                    self.state.next_blocks.remove(self.dragging_block)
                    self.state.next_blocks.append(self.state.block_factory.create_block())
                else:
                    # Reset to original off-board position
                    self.dragging_block.x, self.dragging_block.y = self.original_pos

                self.dragging_block = None
