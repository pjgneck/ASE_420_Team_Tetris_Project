import random
from game.block_data import FIGURES, COLORS

class Block:
    def __init__(self, x: int, y: int):
        """
        Initializes a new Tetris block at the given coordinates.

        :param x: Horizontal position on the board
        :param y: Vertical position on the board
        """
        self.x = x
        self.y = y

        # Choose a random figure type and color (index-based)
        self.type = random.randrange(len(FIGURES))
        self.color = random.randint(1, len(COLORS) - 1) # Don't include (0,0,0)

        self.rotation = 0  # Index of the current rotation state

    def move(self, dx: int, dy: int):
        """
        Moves the block by a given delta.

        :param dx: Change in x-position
        :param dy: Change in y-position
        """
        self.x += dx
        self.y += dy

    def rotate(self):
        """
        Rotates the block clockwise.
        """
        self.rotation = (self.rotation + 1) % len(FIGURES[self.type])

    def undo_rotate(self):
        """
        Rotates the block counter-clockwise (undo last rotation).
        """
        self.rotation = (self.rotation - 1) % len(FIGURES[self.type])
    
    def get_shape(self):
        """
        Returns the current shape (2D array) of the block, depending on its rotation.

        :return: A 2D list representing the block's shape.
        """
        return FIGURES[self.type][self.rotation]

    def get_color(self):
        """
        Returns the color associated with this block.

        :return: An RGB tuple from the COLORS list.
        """
        return COLORS[self.color]
