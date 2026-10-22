# Маппер данных

import uuid

from datasource.models.game_entity import GameEntity
from domain.model.game import Game


class DataMapper:
    """
    Маппер для преобразования моделей между Domain и Datasource
    """

    @staticmethod
    def to_domain(entity: GameEntity) -> Game:
        """
        Из Data в Domain
        """
        return Game(
            id=uuid.UUID(entity.game_id),
            board=entity.board_data,
        )

    @staticmethod
    def to_datasource(game: Game) -> GameEntity:
        """
        Domain -> Data
        """
        return GameEntity(
            game_id=str(game.id),
            board_data=game.board,
        )