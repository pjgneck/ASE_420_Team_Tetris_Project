import random
from game.block import Block
from game.data import SHAPES

class BlockFactory:
    def create_block(self, x: int = 3, y: int = 0) -> Block:
        """
        Creates a new Tetris block at the given position.

        :param x: The starting x-coordinate on the board (default: 3)
        :param y: The starting y-coordinate on the board (default: 0)
        :return: A new Block instance
        """
        block = Block(x, y)
        num_rotations = len(SHAPES[block.shape])
        block.rotate(random.randint(0, num_rotations - 1))
        return block
