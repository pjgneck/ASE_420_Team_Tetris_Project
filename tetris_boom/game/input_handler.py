import pygame

class TetrisInputHandler:
    def __init__(self, game_mode):
        self.game_mode = game_mode

    def handle(self, event):
        block = self.game_mode.block
        board = self.game_mode.board
        factory = self.game_mode.factory

        if event.type == pygame.KEYDOWN:
            if self.game_mode.game_over and event.key == pygame.K_q:
                return "quit"

            if event.key == pygame.K_LEFT:
                block.move(-1, 0)
                if not board.is_valid_position(block):
                    block.move(1, 0)

            elif event.key == pygame.K_RIGHT:
                block.move(1, 0)
                if not board.is_valid_position(block):
                    block.move(-1, 0)

            elif event.key == pygame.K_DOWN:
                self.game_mode.pressing_down = True

            elif event.key == pygame.K_UP:
                block.rotate()
                if not board.is_valid_position(block):
                    block.undo_rotate()

            elif event.key == pygame.K_SPACE:
                while board.is_valid_position(block):
                    block.move(0, 1)
                block.move(0, -1)
                board.freeze(block)
                lines = board.break_lines()
                self.game_mode.score.update(lines)
                self.game_mode.block = factory.create_block()
                if not board.is_valid_position(self.game_mode.block):
                    self.game_mode.game_over = True

        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            self.game_mode.pressing_down = False
