# интерфейсы

from abc import ABC, abstractmethod
import uuid
from typing import Optional
from domain.model.game import Game

class GameRepositoryInterface(ABC):
    """Интерфейс репозитория для управления жизненным циклом игр в хранилище."""

    @abstractmethod
    def save_game(self, game: Game) -> None:
        """Сохраняет или обновляет текущее состояние игры."""
        pass

    @abstractmethod
    def get_game(self, game_id: uuid.UUID) -> Optional[Game]:
        """Возвращает игру по её уникальному UUID идентификатору."""
        pass
