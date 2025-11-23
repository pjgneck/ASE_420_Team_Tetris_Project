import pytest
import os
import json
import tempfile
from unittest.mock import MagicMock, patch, mock_open
from game.score_manager import ScoreManager


class TestScoreManager:
    @pytest.fixture
    def mock_sound_manager(self):
        return MagicMock()

    @pytest.fixture
    def temp_leaderboard_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        yield temp_path
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @patch('game.score_manager.os.path.exists', return_value=False)
    @patch('game.score_manager.getattr')
    @patch('game.score_manager.resource_path')
    def test_score_manager_initialization(self, mock_resource_path, mock_getattr, mock_exists, mock_sound_manager):
        mock_getattr.return_value = False
        mock_resource_path.return_value = "/test/path/highscore.json"
        manager = ScoreManager(mock_sound_manager)
        assert manager.score == 0
        assert manager.leaderboard == []
        assert manager.player_name == ""
        assert manager.sound_manager == mock_sound_manager

    @patch('game.score_manager.os.path.exists', return_value=False)
    def test_set_player_name(self, mock_exists, mock_sound_manager):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value="/test/path/highscore.json"):
                manager = ScoreManager(mock_sound_manager)
                manager.set_player_name("TestPlayer")
                assert manager.player_name == "TestPlayer"

    @patch('game.score_manager.os.path.exists', return_value=False)
    def test_add_points(self, mock_exists, mock_sound_manager):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value="/test/path/highscore.json"):
                manager = ScoreManager(mock_sound_manager)
                manager.add_points(2)
                assert manager.score == 4
                mock_sound_manager.play.assert_any_call("place_block")
                mock_sound_manager.play.assert_any_call("line_clear_1")

    @patch('game.score_manager.os.path.exists', return_value=False)
    def test_add_points_scoring_formula(self, mock_exists, mock_sound_manager):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value="/test/path/highscore.json"):
                manager = ScoreManager(mock_sound_manager)
                manager.add_points(1)
                assert manager.score == 1
                manager.add_points(2)
                assert manager.score == 5
                manager.add_points(3)
                assert manager.score == 14

    @patch('game.score_manager.os.path.exists', return_value=False)
    def test_add_points_sound_selection(self, mock_exists, mock_sound_manager):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value="/test/path/highscore.json"):
                manager = ScoreManager(mock_sound_manager)
                manager.add_points(1)
                mock_sound_manager.play.assert_any_call("line_clear_1")
                manager.add_points(4)
                mock_sound_manager.play.assert_any_call("line_clear_2")
                manager.add_points(11)
                mock_sound_manager.play.assert_any_call("easter_egg")

    @patch('game.score_manager.os.path.exists', return_value=False)
    def test_get_score(self, mock_exists, mock_sound_manager):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value="/test/path/highscore.json"):
                manager = ScoreManager(mock_sound_manager)
                assert manager.get_score() == 0
                manager.add_points(3)
                assert manager.get_score() == 9

    @patch('game.score_manager.os.path.exists', return_value=False)
    def test_reset(self, mock_exists, mock_sound_manager):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value="/test/path/highscore.json"):
                manager = ScoreManager(mock_sound_manager)
                manager.add_points(5)
                manager.reset()
                assert manager.score == 0
                assert manager.highscore_sound_played is False

    @patch('game.score_manager.os.path.exists', return_value=False)
    def test_get_highscore_empty_leaderboard(self, mock_exists, mock_sound_manager):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value="/test/path/highscore.json"):
                manager = ScoreManager(mock_sound_manager)
                assert manager.get_highscore() == 0

    def test_get_highscore_with_entries(self, mock_sound_manager, temp_leaderboard_file):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value=temp_leaderboard_file):
                leaderboard_data = [
                    {"name": "Player1", "score": 100},
                    {"name": "Player2", "score": 50}
                ]
                with open(temp_leaderboard_file, 'w') as f:
                    json.dump(leaderboard_data, f)
                
                manager = ScoreManager(mock_sound_manager)
                assert manager.get_highscore() == 100

    def test_get_highscore_filters_zeros(self, mock_sound_manager, temp_leaderboard_file):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value=temp_leaderboard_file):
                leaderboard_data = [
                    {"name": "Player1", "score": 0},
                    {"name": "Player2", "score": 50}
                ]
                with open(temp_leaderboard_file, 'w') as f:
                    json.dump(leaderboard_data, f)
                
                manager = ScoreManager(mock_sound_manager)
                assert manager.get_highscore() == 50

    @patch('game.score_manager.os.path.exists', return_value=False)
    def test_update_leaderboard_no_zero_scores(self, mock_exists, mock_sound_manager, temp_leaderboard_file):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value=temp_leaderboard_file):
                manager = ScoreManager(mock_sound_manager)
                manager.set_player_name("TestPlayer")
                manager.score = 0
                manager.update_leaderboard()
                
                if os.path.exists(temp_leaderboard_file) and os.path.getsize(temp_leaderboard_file) > 0:
                    with open(temp_leaderboard_file, 'r') as f:
                        content = f.read().strip()
                        if content:
                            data = json.loads(content)
                            assert len(data) == 0
                        else:
                            assert True
                else:
                    assert True

    def test_update_leaderboard_adds_new_player(self, mock_sound_manager, temp_leaderboard_file):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value=temp_leaderboard_file):
                manager = ScoreManager(mock_sound_manager)
                manager.set_player_name("TestPlayer")
                manager.score = 100
                manager.update_leaderboard()
                
                with open(temp_leaderboard_file, 'r') as f:
                    data = json.load(f)
                assert len(data) == 1
                assert data[0]["name"] == "TestPlayer"
                assert data[0]["score"] == 100

    def test_update_leaderboard_updates_existing_player(self, mock_sound_manager, temp_leaderboard_file):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value=temp_leaderboard_file):
                leaderboard_data = [{"name": "TestPlayer", "score": 50}]
                with open(temp_leaderboard_file, 'w') as f:
                    json.dump(leaderboard_data, f)
                
                manager = ScoreManager(mock_sound_manager)
                manager.set_player_name("TestPlayer")
                manager.score = 100
                manager.update_leaderboard()
                
                with open(temp_leaderboard_file, 'r') as f:
                    data = json.load(f)
                assert len(data) == 1
                assert data[0]["score"] == 100

    def test_update_leaderboard_keeps_top_3(self, mock_sound_manager, temp_leaderboard_file):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value=temp_leaderboard_file):
                manager = ScoreManager(mock_sound_manager)
                for i in range(5):
                    manager.set_player_name(f"Player{i}")
                    manager.score = 100 - i * 10
                    manager.update_leaderboard()
                
                with open(temp_leaderboard_file, 'r') as f:
                    data = json.load(f)
                assert len(data) == 3
                assert data[0]["score"] == 100

    @patch('game.score_manager.os.path.exists', return_value=True)
    def test_highscore_sound_only_plays_once(self, mock_exists, mock_sound_manager):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value="/test/path/highscore.json"):
                leaderboard_data = [{"name": "Player", "score": 50}]
                with patch('builtins.open', mock_open(read_data=json.dumps(leaderboard_data))):
                    manager = ScoreManager(mock_sound_manager)
                    manager.score = 60
                    manager.add_points(0)
                    highscore_calls = [call for call in mock_sound_manager.play.call_args_list 
                                     if call[0][0] == "highscore"]
                    assert len(highscore_calls) == 1

    @patch('game.score_manager.os.path.exists', return_value=False)
    def test_highscore_sound_not_played_when_initial_zero(self, mock_exists, mock_sound_manager):
        with patch('game.score_manager.getattr', return_value=False):
            with patch('game.score_manager.resource_path', return_value="/test/path/highscore.json"):
                manager = ScoreManager(mock_sound_manager)
                manager.score = 10
                manager.add_points(0)
                highscore_calls = [call for call in mock_sound_manager.play.call_args_list 
                                 if call[0][0] == "highscore"]
                assert len(highscore_calls) == 0

