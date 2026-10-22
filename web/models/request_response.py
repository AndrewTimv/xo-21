# Модели запросов-ответов

from dataclasses import dataclass


WebBoardMatrix = list[list[int]]


@dataclass
class GameDTO:
    id: str
    board: WebBoardMatrix
    is_over: bool = False
    winner: int | None = None
    error: str | None = None
