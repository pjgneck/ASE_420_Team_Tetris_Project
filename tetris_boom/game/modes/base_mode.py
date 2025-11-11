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

    def _handle_game_over(self, is_game_over: bool=True):
        """
        Handle game over state transitions consistently across all modes.
        Stops background music and plays game over sound when transitioning to game over.
        
        :param new_game_over_state: The new game over state to set
        """
        was_game_over = getattr(self, 'game_over', False)
        self.game_over = is_game_over
        
        # Only trigger sound when transitioning from not-game-over to game-over
        if not was_game_over and self.game_over:
            # Stop background music and play game over sound
            sound_manager = getattr(self.renderer, 'sound_manager', None)
            if sound_manager:
                sound_manager.stop("music_1_loop")
                sound_manager.play("game_over")
