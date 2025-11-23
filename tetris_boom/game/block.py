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

        self.shape = random.choices(range(len(SHAPES)), weights=SHAPE_WEIGHTS, k=1)[0]
        self.color_index = random.randint(1, len(BLOCK_COLORS) - 1)

        self.rotation = 0
        self.is_bomb = False

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

    def get_color(self, theme_colors=None):
        """
        Returns the color associated with this block.

        :return: An RGB tuple from the COLORS list.
        """
        if theme_colors:
            return theme_colors[self.color_index]
        return BLOCK_COLORS[self.color_index]

    def get_cell_count(self):
        """
        Returns the number of cells in the current block shape.
        Used to determine explosion size for bombs.
        """
        return len(self.get_shape())

    def get_explosion_radius(self):
        """
        Calculates the explosion radius for bomb blocks based on cell count.
        Larger blocks create larger explosions.
        """
        if not self.is_bomb:
            return 0
        cell_count = self.get_cell_count()
        return min(4, max(1, (cell_count + 1) // 2))

    def get_board_positions(self):
        """
        Returns a list of (x, y) board coordinates for all cells in this block.
        """
        positions = []
        shape_indices = self.get_shape()
        for idx in shape_indices:
            r = idx // 4
            c = idx % 4
            positions.append((self.x + c, self.y + r))
        return positions

    def copy(self):
        new_block = Block(self.x, self.y)
        new_block.shape = self.shape
        new_block.color_index = self.color_index
        new_block.rotation = self.rotation
        new_block.is_bomb = self.is_bomb
        new_block.screen_x = getattr(self, 'screen_x', 0)
        new_block.screen_y = getattr(self, 'screen_y', 0)
        return new_block
