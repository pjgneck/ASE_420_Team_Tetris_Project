from game.block import BLOCK_COLORS
from game.data import BLOCK_GRID_SIZE

class Board:
    def __init__(self, rows=20, cols=10):
        """
        Initializes the game board with specified rows and columns.

        :param rows: The number of rows on the board (default is 20)
        :param cols: The number of columns on the board (default is 10)
        """
        self.rows = rows
        self.cols = cols
        self.BLOCK_COLORS = BLOCK_COLORS
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def is_valid_position(self, block):
        """
        Checks if the given block's position is valid on the board.

        :param block: The block to check
        :return: True if the block's position is valid, otherwise False
        """
        for i in range(BLOCK_GRID_SIZE):
            for j in range(BLOCK_GRID_SIZE):
                if i * BLOCK_GRID_SIZE + j in block.get_shape():
                    x = block.x + j
                    y = block.y + i
                    if x < 0 or x >= self.cols or y >= self.rows:
                        return False
                    if y >= 0 and self.grid[y][x] > 0:
                        return False
        return True

    def freeze(self, block):
        """
        Freezes the given block into the board when it reaches the bottom.

        :param block: The block to freeze
        """
        for i in range(BLOCK_GRID_SIZE):
            for j in range(BLOCK_GRID_SIZE):
                if i * BLOCK_GRID_SIZE + j in block.get_shape():
                    x = block.x + j
                    y = block.y + i
                    if y >= 0:
                        self.grid[y][x] = block.color_index

    def break_lines(self):
        """
        Checks for full lines and clears them. Newly empty lines are added to the top.

        :return: The number of lines cleared
        """
        lines_cleared = 0
        new_grid = []

        for row in self.grid:
            if all(cell > 0 for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)

        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.cols)])

        self.grid = new_grid
        return lines_cleared
    
    def has_space_for_block(self, block):
        """
        Checks if the given block can be placed anywhere on the board.
        """
        for y in range(self.rows):
            for x in range(self.cols):
                block.x = x
                block.y = y
                if self.is_valid_position(block):
                    return True
        return False
