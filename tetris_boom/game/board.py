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
        Checks for full lines (rows and columns) and clears them.

        :return: The number of lines cleared
        """
        lines_cleared = 0
        
        rows_to_clear = []
        for i, row in enumerate(self.grid):
            if all(cell > 0 for cell in row):
                rows_to_clear.append(i)
                lines_cleared += 1
        
        cols_to_clear = []
        for j in range(self.cols):
            if all(self.grid[i][j] > 0 for i in range(self.rows)):
                cols_to_clear.append(j)
                lines_cleared += 1
        
        new_grid = []
        for i, row in enumerate(self.grid):
            if i not in rows_to_clear:
                new_row = [0 if j in cols_to_clear else cell for j, cell in enumerate(row)]
                new_grid.append(new_row)
        
        for _ in range(len(rows_to_clear)):
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

    def explode_area(self, center_x: int, center_y: int, radius: int = 1):
        """
        Clears an area centered on the given coordinates.
        The area is (2*radius + 1) x (2*radius + 1).
        
        :param center_x: X coordinate of explosion center
        :param center_y: Y coordinate of explosion center
        :param radius: Explosion radius (default 1 for 3x3 area)
        :return: Number of blocks cleared
        """
        blocks_cleared = 0
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                x = center_x + dx
                y = center_y + dy
                if 0 <= x < self.cols and 0 <= y < self.rows:
                    if self.grid[y][x] > 0:
                        blocks_cleared += 1
                    self.grid[y][x] = 0
        return blocks_cleared

    def explode_bomb(self, block):
        """
        Explodes a bomb block, clearing areas around each cell in the block.
        
        :param block: The bomb block to explode
        :return: Total number of blocks cleared
        """
        if not block.is_bomb:
            return 0
        
        explosion_radius = block.get_explosion_radius()
        total_cleared = 0
        
        for center_x, center_y in block.get_board_positions():
            if 0 <= center_y < self.rows and 0 <= center_x < self.cols:
                total_cleared += self.explode_area(center_x, center_y, explosion_radius)
        
        return total_cleared
