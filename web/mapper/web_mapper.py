# Преобразование web в domain

import uuid
from web.models.request_response import GameDTO
from domain.model.game import Game

class WebMapper:
    """
    преобразование моделей между Domain и Web слоями
    """

    @staticmethod
    def to_domain(dto: GameDTO) -> Game:
        """
        DTO от клиента в доменную модель игры
        """
        return Game(
            id=uuid.UUID(dto.id),
            board=dto.board
        )

    @staticmethod
    def to_dto(domain_game: Game, is_over: bool = False, winner: int | None = None) -> GameDTO:
        """
        доменная модель игры в DTO
        """
        return GameDTO(
            id=str(domain_game.id),
            board=domain_game.board,
            is_over=is_over,
            winner=winner
        )
