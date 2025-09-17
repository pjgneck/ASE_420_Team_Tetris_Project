from game.block import Block

class BlockFactory:
    def create_block(self, x=3, y=0):
        return Block(x, y)
