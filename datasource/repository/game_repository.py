# Репо

import uuid
from typing import Optional
from domain.model.game import Game
from datasource.repository.game_repository_interfaces import GameRepositoryInterface
from datasource.repository.storage import InMemoryStorage
from datasource.mapper.data_mapper import DataMapper

class GameRepository(GameRepositoryInterface):
    """Реализация репозитория, работающая с In-Memory хранилищем."""

    def __init__(self, storage: InMemoryStorage):
        self._storage = storage

    def save_game(self, game: Game) -> None:
        entity = DataMapper.to_datasource(game)
        self._storage.save(entity)

    def get_game(self, game_id: uuid.UUID) -> Optional[Game]:
        entity = self._storage.get(str(game_id))
        if entity is None:
            return None
        return DataMapper.to_domain(entity)
