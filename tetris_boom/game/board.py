from game.block import COLORS

class Board:
    def __init__(self, rows=20, cols=10):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.COLORS = COLORS

    def is_valid_position(self, block):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in block.get_image():
                    x = block.x + j
                    y = block.y + i
                    if x < 0 or x >= self.cols or y >= self.rows:
                        return False
                    if y >= 0 and self.grid[y][x] > 0:
                        return False
        return True

    def freeze(self, block):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in block.get_image():
                    x = block.x + j
                    y = block.y + i
                    if y >= 0:
                        self.grid[y][x] = block.color

    def break_lines(self):
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
