# Модели хранения данных

from dataclasses import dataclass


@dataclass
class GameEntity:
    """
    Модель игры для слоя данных
    """
    game_id: str
    board_data: list[list[int]]