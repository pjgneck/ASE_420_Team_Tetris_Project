import pytest
import sys
import os
from unittest.mock import MagicMock, Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tetris_boom'))

@pytest.fixture
def mock_sound_manager():
    return MagicMock()

@pytest.fixture
def mock_pygame():
    pygame_mock = MagicMock()
    sys.modules['pygame'] = pygame_mock
    return pygame_mock

