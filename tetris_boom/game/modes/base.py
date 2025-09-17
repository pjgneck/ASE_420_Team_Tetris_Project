from abc import ABC, abstractmethod

class GameMode(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def handle_input(self, event):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def spawn_piece(self, event):
        pass
