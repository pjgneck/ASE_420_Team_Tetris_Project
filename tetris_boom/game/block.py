import random
from game.data import SHAPES, SHAPE_WEIGHTS, BLOCK_COLORS

class Block:
    def __init__(self, x: int, y: int):
        """
        Initializes a new Tetris block at the given coordinates.

        :param x: Horizontal position on the board
        :param y: Vertical position on the board
        """
        self.x = x
        self.y = y

        # Choose a random shape and color (index-based)
        self.shape = random.choices(range(len(SHAPES)), weights=SHAPE_WEIGHTS, k=1)[0]
        self.color = random.randint(1, len(BLOCK_COLORS) - 1) # 0 is reservered for empty space

        self.rotation = 0  # Index of the current rotation state

    def move(self, dx: int, dy: int):
        """
        Moves the block by a given delta.

        :param dx: Change in x-position
        :param dy: Change in y-position
        """
        self.x += dx
        self.y += dy

    def rotate(self, times=1):
        """
        Rotates the block clockwise.
        """
        self.rotation = (self.rotation + times) % len(SHAPES[self.shape])


    def undo_rotate(self):
        """
        Rotates the block counter-clockwise (undo last rotation).
        """
        self.rotation = (self.rotation - 1) % len(SHAPES[self.shape])
    
    def get_shape(self):
        """
        Returns the current shape (2D array) of the block, depending on its rotation.

        :return: A 2D list representing the block's shape.
        """
        return SHAPES[self.shape][self.rotation]

    def get_color(self):
        """
        Returns the color associated with this block.

        :return: An RGB tuple from the COLORS list.
        """
        return BLOCK_COLORS[self.color]

    def copy(self):
        new_block = Block(self.x, self.y)
        new_block.shape = self.shape
        new_block.color = self.color
        new_block.rotation = self.rotation
        new_block.screen_x = getattr(self, 'screen_x', 0)
        new_block.screen_y = getattr(self, 'screen_y', 0)
        return new_block
