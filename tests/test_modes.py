import pytest
from unittest.mock import MagicMock, Mock
import pygame
from game.modes.tetris_mode import TetrisMode
from game.modes.blockblast_mode import BlockBlastMode
from game.modes.base_mode import GameMode
from game.gamestate import GameState
from game.board import Board
from game.block_factory import BlockFactory
from game.score_manager import ScoreManager
from game.sound_manager import SoundManager


class TestTetrisMode:
    @pytest.fixture
    def mock_screen(self):
        return MagicMock()

    @pytest.fixture
    def mock_state(self):
        board = Board()
        block_factory = BlockFactory()
        score_manager = MagicMock(spec=ScoreManager)
        sound_manager = MagicMock(spec=SoundManager)
        state = GameState(board, block_factory, score_manager, sound_manager)
        return state

    @pytest.fixture
    def mock_renderer(self):
        return MagicMock()

    def test_tetris_mode_initialization(self, mock_screen, mock_state, mock_renderer):
        mode = TetrisMode(mock_screen, mock_state, mock_renderer)
        assert mode.screen == mock_screen
        assert mode.state == mock_state
        assert mode.renderer == mock_renderer
        assert mode.game_over is False
        assert mode.gravity == 1.5
        assert mode.fall_timer == 0.0
        assert mode.pressing_down is False

    def test_tetris_mode_should_show_cursor(self, mock_screen, mock_state, mock_renderer):
        mode = TetrisMode(mock_screen, mock_state, mock_renderer)
        assert mode.should_show_cursor() is False

    def test_tetris_mode_update_when_game_over(self, mock_screen, mock_state, mock_renderer):
        mode = TetrisMode(mock_screen, mock_state, mock_renderer)
        mode.game_over = True
        initial_fall_timer = mode.fall_timer
        mode.update()
        assert mode.fall_timer == initial_fall_timer

    def test_tetris_mode_spawn_block(self, mock_screen, mock_state, mock_renderer):
        mode = TetrisMode(mock_screen, mock_state, mock_renderer)
        old_block = mode.state.current_block
        mode.spawn_block()
        assert mode.state.current_block is not old_block


class TestBlockBlastMode:
    @pytest.fixture
    def mock_screen(self):
        return MagicMock()

    @pytest.fixture
    def mock_state(self):
        board = Board()
        block_factory = BlockFactory()
        score_manager = MagicMock(spec=ScoreManager)
        sound_manager = MagicMock(spec=SoundManager)
        state = GameState(board, block_factory, score_manager, sound_manager)
        return state

    @pytest.fixture
    def mock_renderer(self):
        return MagicMock()

    def test_blockblast_mode_initialization(self, mock_screen, mock_state, mock_renderer):
        mode = BlockBlastMode(mock_screen, mock_state, mock_renderer)
        assert mode.screen == mock_screen
        assert mode.state == mock_state
        assert mode.renderer == mock_renderer
        assert mode.game_over is False

    def test_blockblast_mode_should_show_cursor(self, mock_screen, mock_state, mock_renderer):
        mode = BlockBlastMode(mock_screen, mock_state, mock_renderer)
        assert mode.should_show_cursor() is True

    def test_blockblast_mode_spawn_block(self, mock_screen, mock_state, mock_renderer):
        mode = BlockBlastMode(mock_screen, mock_state, mock_renderer)
        mode.spawn_block()
        assert True

    def test_blockblast_mode_update_game_over_when_no_space(self, mock_screen, mock_state, mock_renderer):
        mode = BlockBlastMode(mock_screen, mock_state, mock_renderer)
        for i in range(mode.state.board.rows):
            for j in range(mode.state.board.cols):
                mode.state.board.grid[i][j] = 1
        mode.update()
        assert mode.game_over is True


class TestGameModeBase:
    def test_should_show_cursor_default(self):
        class TestMode(GameMode):
            def update(self):
                pass
            def handle_input(self, event):
                pass
            def render(self):
                pass
            def spawn_block(self):
                pass
        
        mode = TestMode()
        assert mode.should_show_cursor() is True

