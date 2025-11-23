import pytest
from game.block_factory import BlockFactory
from game.block import Block
from game.data import SHAPES


class TestBlockFactory:
    def test_create_block_default_position(self):
        factory = BlockFactory()
        block = factory.create_block()
        assert block.x == 3
        assert block.y == 0
        assert isinstance(block, Block)

    def test_create_block_custom_position(self):
        factory = BlockFactory()
        block = factory.create_block(x=5, y=10)
        assert block.x == 5
        assert block.y == 10

    def test_create_block_has_shape(self):
        factory = BlockFactory()
        block = factory.create_block()
        assert block.shape >= 0
        assert block.shape < len(SHAPES)

    def test_create_block_has_rotation(self):
        factory = BlockFactory()
        block = factory.create_block()
        num_rotations = len(SHAPES[block.shape])
        assert block.rotation >= 0
        assert block.rotation < num_rotations

    def test_create_block_has_color(self):
        factory = BlockFactory()
        block = factory.create_block()
        assert block.color_index >= 1

