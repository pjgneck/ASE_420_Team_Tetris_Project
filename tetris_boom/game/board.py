from game.block import BLOCK_COLORS

class Board:
    def __init__(self, rows=20, cols=10):
        """
        Initializes the game board with specified rows and columns.

        :param rows: The number of rows on the board (default is 20)
        :param cols: The number of columns on the board (default is 10)
        """
        self.rows = rows
        self.cols = cols
        self.BLOCK_COLORS = BLOCK_COLORS  # Block colors (imported from game.block)
        # Initialize the grid with 0s (empty spaces)
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def is_valid_position(self, block):
        """
        Checks if the given block's position is valid on the board.

        :param block: The block to check
        :return: True if the block's position is valid, otherwise False
        """
        for i in range(4):  # Iterate over the 4x4 block grid
            for j in range(4):
                if i * 4 + j in block.get_shape():  # Check if the cell is part of the block
                    x = block.x + j  # x-position of the block part
                    y = block.y + i  # y-position of the block part
                    if x < 0 or x >= self.cols or y >= self.rows:
                        return False  # Block goes out of bounds
                    if y >= 0 and self.grid[y][x] > 0:
                        return False  # Block overlaps with an existing block
        return True  # The block's position is valid

    def freeze(self, block):
        """
        Freezes the given block into the board when it reaches the bottom.

        :param block: The block to freeze
        """
        for i in range(4):  # Iterate over the 4x4 block grid
            for j in range(4):
                if i * 4 + j in block.get_shape():  # Check if the cell is part of the block
                    x = block.x + j  # x-position of the block part
                    y = block.y + i  # y-position of the block part
                    if y >= 0:  # Avoid updating negative y-values (above the board)
                        self.grid[y][x] = block.color_index  # Set the block's color in the grid

    def break_lines(self):
        """
        Checks for full lines and clears them. Newly empty lines are added to the top.

        :return lines_cleared: The number of lines cleared
        """
        lines_cleared = 0
        new_grid = []  # New grid without cleared lines

        for row in self.grid:
            if all(cell > 0 for cell in row):  # Check if the row is full (all cells are filled)
                lines_cleared += 1  # Increment the number of cleared lines
            else:
                new_grid.append(row)  # Keep the row if it's not full

        # Add empty rows at the top of the grid to fill the cleared lines
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(self.cols)])

        self.grid = new_grid  # Update the board's grid
        return lines_cleared  # Return the number of cleared lines
    
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
