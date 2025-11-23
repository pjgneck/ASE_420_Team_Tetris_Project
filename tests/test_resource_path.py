import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from game.resource_path import resource_path


class TestResourcePath:
    def test_resource_path_development_mode(self):
        if hasattr(sys, '_MEIPASS'):
            original = sys._MEIPASS
            delattr(sys, '_MEIPASS')
        try:
            result = resource_path("assets/sounds")
            assert "assets/sounds" in result
            assert os.path.isabs(result)
        finally:
            if 'original' in locals():
                sys._MEIPASS = original

    def test_resource_path_pyinstaller_mode(self):
        with patch.object(sys, '_MEIPASS', '/tmp/pyinstaller_temp', create=True):
            result = resource_path("assets/sounds")
            expected = os.path.join("/tmp/pyinstaller_temp", "tetris_boom", "assets/sounds")
            assert result == expected

    def test_resource_path_different_paths(self):
        with patch.object(sys, '_MEIPASS', '/tmp/pyinstaller_temp', create=True):
            result1 = resource_path("assets/sounds")
            result2 = resource_path("assets/highscore.json")
            assert result1 != result2
            assert "sounds" in result1
            assert "highscore.json" in result2

