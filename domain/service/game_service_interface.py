# Интерфейсы сервиса

from abc import ABC, abstractmethod
from typing import Any

from domain.model.game import Game, Board


class GameServiceInterface(ABC):
    """
    Интерфейс сервиса для управления бизнес-логикой
    """
    @abstractmethod
    def __init__(self, repository: Any):
        pass

    @abstractmethod
    def get_move(self, current_game: Game, bot: int) -> tuple[int, int] | None:
        """
        Вычисляет оптимальный алгоритм для бота
        :param current_game: текущая игра
        :param bot: 1 - X, 2 - O
        :return: координаты или None
        """
        pass


    @abstractmethod
    def validate_board(self, current_game: Game, new_board: Board) -> bool:
        """
        Проверка, что на новом поле не изменены старые значения
        :param current_game: текущее состояние игры
        :param new_board: новая матрица поля от клиента
        :return: True, если всё хорошо, иначе False
        """
        pass


    @abstractmethod
    def check_game_over(self, board: Board) -> tuple[bool, int | None]:
        """
        Проверяет, что игра закончилась.
        :param board: Игровое поле.
        :return: кортеж (is_over, winner), где winner 1 - X, 2 - O
        """
        pass
