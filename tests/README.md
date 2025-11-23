# Test Suite

This directory contains comprehensive unit tests for the Tetris BOOM game.

## Running Tests

Install dependencies:
```bash
pip install -r requirements.txt
```

Run all tests:
```bash
pytest tests/
```

Run with verbose output:
```bash
pytest tests/ -v
```

Run a specific test file:
```bash
pytest tests/test_board.py
```

Run a specific test:
```bash
pytest tests/test_board.py::TestBoard::test_board_initialization
```

## Test Coverage

The test suite covers:

- **Board** (`test_board.py`): Line clearing (horizontal and vertical), block placement, validation, space checking
- **Block** (`test_block.py`): Movement, rotation, shape retrieval, color handling, copying
- **BlockFactory** (`test_block_factory.py`): Block creation with proper initialization
- **ScoreManager** (`test_score_manager.py`): Scoring, leaderboard management, highscore tracking, zero score filtering
- **GameState** (`test_gamestate.py`): State initialization and management
- **Modes** (`test_modes.py`): TetrisMode and BlockBlastMode functionality, cursor visibility
- **ResourcePath** (`test_resource_path.py`): Path resolution for development and PyInstaller bundles

## Test Structure

Tests use pytest fixtures for setup and mocking. The `conftest.py` file provides shared fixtures for mocking pygame and sound managers.

