# Потокобезопасное хранилище

import threading

from datasource.models.game_entity import GameEntity


class InMemoryStorage:
    """
    Потокобезопасное In-Memory хранилище
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Singleton
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(InMemoryStorage, cls).__new__(cls)
                cls._instance._games = {}
        return cls._instance


    def save(self, entity: GameEntity) -> None:
        with self._lock:
            copied_board = [row[:] for row in entity.board_data]
            self._games[entity.game_id] = GameEntity(
                game_id=entity.game_id,
                board_data=copied_board
            )


    def get(self, game_id: str) -> GameEntity | None:
        with self._lock:
            entity = self._games.get(game_id)
            if not entity:
                return None
            copied_board = [row[:] for row in entity.board_data]
            return GameEntity(game_id=entity.game_id, board_data=copied_board)
