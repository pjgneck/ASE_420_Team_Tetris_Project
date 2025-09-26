from game.score_manager import ScoreManager

class GameState:
    def __init__(self, board, block_factory):
        self.board = board
        self.block_factory = block_factory
        self.score_manager = ScoreManager()
        self.current_block = self.block_factory.create_block()
        self.block_pool = [block_factory.create_block() for _ in range(3)]  # Pool for BlockBlast
        self.selected_block = None
        self.preview_position = None
        self.game_over = False
        self.next_blocks = []
