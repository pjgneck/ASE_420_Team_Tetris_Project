import pygame
from game.data import BLOCK_SIZE
from game.input_handlers.base_input_handler import BaseInputHandler
from game.modes.base_mode import GameMode

class BlockBlastInputHandler(BaseInputHandler):
    def __init__(self, blockblast_mode: GameMode):
        super().__init__(blockblast_mode)
        self.blockblast_mode = blockblast_mode
        self.dragging_block = None
        self.drag_offset = (0, 0)
        self.original_pos = (0, 0)
        self.preview_pos = None

    def handle(self, event):
        renderer = self.blockblast_mode.renderer
        
        # Stop processing input if game is over
        if self.blockblast_mode.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return "quit"
            return  # Ignore all other input when game over
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._start_drag(event, renderer)

        elif event.type == pygame.MOUSEMOTION:
            self._drag(event, renderer)

        elif event.type == pygame.MOUSEBUTTONUP:
            self._drop(renderer)

    # ---- Internal helper methods ----

    def _start_drag(self, event, renderer):
        for idx, block in enumerate(self.state.next_blocks[:3]):
            start_x = renderer.offset_x + self.board.cols * BLOCK_SIZE + 50
            start_y = renderer.offset_y + idx * 100
            cells = [(k // 4, k % 4) for k in block.get_shape()]

            min_i = min(i for i, j in cells)
            min_j = min(j for i, j in cells)
            max_i = max(i for i, j in cells)
            max_j = max(j for i, j in cells)

            rect = pygame.Rect(
                start_x + min_j * BLOCK_SIZE,
                start_y + min_i * BLOCK_SIZE,
                (max_j - min_j + 1) * BLOCK_SIZE,
                (max_i - min_i + 1) * BLOCK_SIZE
            )

            if rect.collidepoint(event.pos):
                self.dragging_block = block
                self.drag_offset = (rect.x - event.pos[0], rect.y - event.pos[1])
                self.original_pos = (block.x, block.y)
                block.screen_x = event.pos[0] + self.drag_offset[0]
                block.screen_y = event.pos[1] + self.drag_offset[1]
                self.preview_pos = None
                break

    def _drag(self, event, renderer):
        if not self.dragging_block:
            return

        self.dragging_block.screen_x = event.pos[0] + self.drag_offset[0]
        self.dragging_block.screen_y = event.pos[1] + self.drag_offset[1]

        grid_x = (self.dragging_block.screen_x - renderer.offset_x) // BLOCK_SIZE
        grid_y = (self.dragging_block.screen_y - renderer.offset_y) // BLOCK_SIZE

        preview_block = self.dragging_block.copy()
        preview_block.x = grid_x
        preview_block.y = grid_y

        self.preview_pos = (grid_x, grid_y) if self.is_valid(preview_block) else None

    def _drop(self, renderer):
        if not self.dragging_block:
            return

        grid_x, grid_y = renderer.compute_snapped_preview(self.dragging_block)
        self.dragging_block.x = grid_x
        self.dragging_block.y = grid_y

        if self.is_valid(self.dragging_block):
            self.freeze_block(self.dragging_block)
            self.state.next_blocks.remove(self.dragging_block)
            self.state.next_blocks.append(self.state.block_factory.create_block())
        else:
            self.dragging_block.x, self.dragging_block.y = self.original_pos

        self.dragging_block = None
