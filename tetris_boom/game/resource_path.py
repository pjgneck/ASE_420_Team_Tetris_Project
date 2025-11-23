"""
Utility module for resolving resource paths that work in both development and PyInstaller bundles.
"""
import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource file.
    
    Works for both development and PyInstaller bundled environments.
    When running from a PyInstaller bundle, sys._MEIPASS contains the path
    to the temporary folder where PyInstaller extracts bundled files.
    
    :param relative_path: Path relative to the tetris_boom directory (e.g., "assets/sounds")
    :return: Absolute path to the resource
    """
    try:
        base_path = os.path.join(sys._MEIPASS, "tetris_boom")
    except AttributeError:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)

