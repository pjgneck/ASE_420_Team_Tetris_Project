import pytest
from game.board import Board
from game.block import Block
from game.data import SHAPES


class TestBoard:
    def test_board_initialization(self):
        board = Board(rows=20, cols=10)
        assert board.rows == 20
        assert board.cols == 10
        assert len(board.grid) == 20
        assert len(board.grid[0]) == 10
        assert all(cell == 0 for row in board.grid for cell in row)

    def test_board_custom_size(self):
        board = Board(rows=15, cols=8)
        assert board.rows == 15
        assert board.cols == 8
        assert len(board.grid) == 15
        assert len(board.grid[0]) == 8

    def test_is_valid_position_valid(self):
        board = Board()
        block = Block(3, 0)
        block.shape = 0
        block.rotation = 0
        assert board.is_valid_position(block) is True

    def test_is_valid_position_out_of_bounds_left(self):
        board = Board()
        block = Block(-1, 0)
        block.shape = 3
        block.rotation = 1
        assert board.is_valid_position(block) is False

    def test_is_valid_position_out_of_bounds_right(self):
        board = Board()
        block = Block(10, 0)
        block.shape = 0
        block.rotation = 0
        assert board.is_valid_position(block) is False

    def test_is_valid_position_out_of_bounds_bottom(self):
        board = Board()
        block = Block(3, 20)
        block.shape = 0
        block.rotation = 0
        assert board.is_valid_position(block) is False

    def test_is_valid_position_overlaps_existing_block(self):
        board = Board()
        block = Block(4, 5)
        block.shape = 0
        block.rotation = 0
        shape = block.get_shape()
        for idx in shape:
            r = idx // 4
            c = idx % 4
            x = block.x + c
            y = block.y + r
            board.grid[y][x] = 1
        block2 = Block(4, 5)
        block2.shape = 0
        block2.rotation = 0
        assert board.is_valid_position(block2) is False

    def test_freeze_block(self):
        board = Board()
        block = Block(4, 5)
        block.shape = 0
        block.rotation = 0
        block.color_index = 2
        board.freeze(block)
        assert board.grid[5][5] == 2
        assert board.grid[6][5] == 2
        assert board.grid[7][5] == 2
        assert board.grid[8][5] == 2

    def test_freeze_block_above_board(self):
        board = Board()
        block = Block(3, -1)
        block.shape = 0
        block.rotation = 0
        block.color_index = 2
        board.freeze(block)
        assert board.grid[0][3] == 0

    def test_break_lines_horizontal_single(self):
        board = Board(rows=5, cols=5)
        for j in range(5):
            board.grid[2][j] = 1
        lines_cleared = board.break_lines()
        assert lines_cleared == 1
        assert all(cell == 0 for cell in board.grid[0])

    def test_break_lines_horizontal_multiple(self):
        board = Board(rows=5, cols=5)
        for i in [1, 2]:
            for j in range(5):
                board.grid[i][j] = 1
        lines_cleared = board.break_lines()
        assert lines_cleared == 2
        assert all(cell == 0 for cell in board.grid[0])
        assert all(cell == 0 for cell in board.grid[1])

    def test_break_lines_vertical_single(self):
        board = Board(rows=5, cols=5)
        for i in range(5):
            board.grid[i][2] = 1
        lines_cleared = board.break_lines()
        assert lines_cleared == 1
        assert all(board.grid[i][2] == 0 for i in range(5))

    def test_break_lines_vertical_multiple(self):
        board = Board(rows=5, cols=5)
        for j in [1, 2]:
            for i in range(5):
                board.grid[i][j] = 1
        lines_cleared = board.break_lines()
        assert lines_cleared == 2
        assert all(board.grid[i][1] == 0 for i in range(5))
        assert all(board.grid[i][2] == 0 for i in range(5))

    def test_break_lines_horizontal_and_vertical(self):
        board = Board(rows=5, cols=5)
        for j in range(5):
            board.grid[2][j] = 1
        for i in range(5):
            board.grid[i][2] = 1
        lines_cleared = board.break_lines()
        assert lines_cleared == 2
        assert all(cell == 0 for cell in board.grid[0])
        assert all(board.grid[i][2] == 0 for i in range(5))

    def test_break_lines_no_lines(self):
        board = Board()
        board.grid[5][5] = 1
        lines_cleared = board.break_lines()
        assert lines_cleared == 0
        assert board.grid[5][5] == 1

    def test_has_space_for_block_with_space(self):
        board = Board()
        block = Block(0, 0)
        block.shape = 0
        block.rotation = 0
        assert board.has_space_for_block(block) is True

    def test_has_space_for_block_no_space(self):
        board = Board()
        for i in range(board.rows):
            for j in range(board.cols):
                board.grid[i][j] = 1
        block = Block(0, 0)
        block.shape = 0
        block.rotation = 0
        assert board.has_space_for_block(block) is False

