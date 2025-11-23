import pytest
from unittest.mock import MagicMock
from game.gamestate import GameState
from game.board import Board
from game.block_factory import BlockFactory
from game.score_manager import ScoreManager
from game.sound_manager import SoundManager


class TestGameState:
    @pytest.fixture
    def mock_components(self):
        board = Board()
        block_factory = BlockFactory()
        score_manager = MagicMock(spec=ScoreManager)
        sound_manager = MagicMock(spec=SoundManager)
        return board, block_factory, score_manager, sound_manager

    def test_gamestate_initialization(self, mock_components):
        board, block_factory, score_manager, sound_manager = mock_components
        state = GameState(board, block_factory, score_manager, sound_manager)
        
        assert state.board == board
        assert state.block_factory == block_factory
        assert state.score_manager == score_manager
        assert state.sound_manager == sound_manager
        assert state.current_block is not None
        assert state.next_blocks == []
        assert state.selected_block is None
        assert state.preview_position is None
        assert state.game_over is False

    def test_gamestate_creates_initial_block(self, mock_components):
        board, block_factory, score_manager, sound_manager = mock_components
        state = GameState(board, block_factory, score_manager, sound_manager)
        
        assert state.current_block is not None
        assert state.current_block.x == 3
        assert state.current_block.y == 0

