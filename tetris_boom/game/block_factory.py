from game.block import Block

class BlockFactory:
    def create_block(self, x: int = 3, y: int = 0) -> Block:
        """
        Creates a new Tetris block at the given position.

        :param x: The starting x-coordinate on the board (default: 3)
        :param y: The starting y-coordinate on the board (default: 0)
        :return: A new Block instance
        """
        return Block(x, y)
