import pytest
from game.block import Block
from game.data import SHAPES, BLOCK_COLORS


class TestBlock:
    def test_block_initialization(self):
        block = Block(5, 10)
        assert block.x == 5
        assert block.y == 10
        assert block.shape >= 0
        assert block.shape < len(SHAPES)
        assert block.color_index >= 1
        assert block.color_index < len(BLOCK_COLORS)
        assert block.rotation == 0

    def test_block_move(self):
        block = Block(3, 5)
        block.move(2, 3)
        assert block.x == 5
        assert block.y == 8

    def test_block_move_negative(self):
        block = Block(5, 10)
        block.move(-2, -3)
        assert block.x == 3
        assert block.y == 7

    def test_block_rotate(self):
        block = Block(0, 0)
        block.shape = 0
        initial_rotation = block.rotation
        num_rotations = len(SHAPES[block.shape])
        block.rotate()
        assert block.rotation == (initial_rotation + 1) % num_rotations

    def test_block_rotate_wraps_around(self):
        block = Block(0, 0)
        block.shape = 0
        num_rotations = len(SHAPES[block.shape])
        for _ in range(num_rotations):
            block.rotate()
        assert block.rotation == 0

    def test_block_undo_rotate(self):
        block = Block(0, 0)
        block.shape = 0
        block.rotation = 1
        num_rotations = len(SHAPES[block.shape])
        block.undo_rotate()
        assert block.rotation == 0

    def test_block_undo_rotate_wraps_around(self):
        block = Block(0, 0)
        block.shape = 0
        block.rotation = 0
        num_rotations = len(SHAPES[block.shape])
        block.undo_rotate()
        assert block.rotation == num_rotations - 1

    def test_get_shape(self):
        block = Block(0, 0)
        block.shape = 0
        block.rotation = 0
        shape = block.get_shape()
        assert shape == SHAPES[0][0]

    def test_get_shape_different_rotation(self):
        block = Block(0, 0)
        block.shape = 0
        block.rotation = 1
        shape = block.get_shape()
        assert shape == SHAPES[0][1]

    def test_get_color_default(self):
        block = Block(0, 0)
        block.color_index = 1
        color = block.get_color()
        assert color == BLOCK_COLORS[1]

    def test_get_color_theme(self):
        block = Block(0, 0)
        block.color_index = 1
        theme_colors = {1: (255, 0, 0), 2: (0, 255, 0)}
        color = block.get_color(theme_colors)
        assert color == (255, 0, 0)

    def test_block_copy(self):
        block = Block(5, 10)
        block.shape = 2
        block.color_index = 3
        block.rotation = 1
        block.screen_x = 100
        block.screen_y = 200
        
        copied = block.copy()
        assert copied.x == block.x
        assert copied.y == block.y
        assert copied.shape == block.shape
        assert copied.color_index == block.color_index
        assert copied.rotation == block.rotation
        assert copied.screen_x == block.screen_x
        assert copied.screen_y == block.screen_y
        assert copied is not block

    def test_block_copy_no_screen_coords(self):
        block = Block(5, 10)
        block.shape = 2
        block.color_index = 3
        block.rotation = 1
        
        copied = block.copy()
        assert copied.screen_x == 0
        assert copied.screen_y == 0

