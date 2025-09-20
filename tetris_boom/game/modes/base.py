from abc import ABC, abstractmethod
import pygame

class GameMode(ABC):
    @abstractmethod
    def update(self):
        """
        Update the game state (called each frame).
        """
        pass

    @abstractmethod
    def handle_input(self, event: pygame.event.Event):
        """
        Handle player input.

        :param event: A pygame event (e.g. key press)
        """
        pass

    @abstractmethod
    def render(self):
        """
        Render the game state to the screen.
        """
        pass

    @abstractmethod
    def spawn_block(self):
        """
        Spawn a new block in the game.
        """
        pass
