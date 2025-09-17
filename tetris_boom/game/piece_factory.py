from game.block import Block

class PieceFactory:
    def create_block(self, x=3, y=0):
        return Block(x, y)
