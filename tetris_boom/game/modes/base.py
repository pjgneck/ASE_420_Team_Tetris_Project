from abc import ABC, abstractmethod

class GameMode(ABC):
    @abstractmethod
    def update(self): pass

    @abstractmethod
    def handle_input(self): pass

    @abstractmethod
    def render(self, renderer): pass

    @abstractmethod
    def spawn_piece(self): pass
