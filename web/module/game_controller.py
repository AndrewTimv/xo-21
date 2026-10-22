# Управление игрой

import uuid
from typing import Tuple, Dict, Any

from datasource.repository.game_repository_interfaces import GameRepositoryInterface
from domain.service.game_service_interface import GameServiceInterface
from web.mapper.web_mapper import WebMapper


class GameController:
    """Контроллер, управляющий игровым процессом на веб-слое."""

    def __init__(self, game_service: GameServiceInterface, game_repository: GameRepositoryInterface):
        self._game_service = game_service
        self._game_repository = game_repository

    def handle_player_move(self, game_id_str: str, client_board: list) -> Tuple[Dict[str, Any], int]:
        """
        Обрабатывает ход игрока, валидирует его, делает ответный ход бота
        и возвращает обновленное состояние игры или ошибку.
        """
        try:
            game_id = uuid.UUID(game_id_str)
        except ValueError:
            return {"error": "Некорректный формат UUID игры"}, 400

        current_game = self._game_repository.get_game(game_id)
        if not current_game:
            return {"error": "Игра с указанным UUID не найдена"}, 404

        already_over, saved_winner = self._game_service.check_game_over(current_game.board)
        if already_over:
            dto = WebMapper.to_dto(current_game, is_over=True, winner=saved_winner)
            return dto.__dict__, 200

        if not self._game_service.validate_board(current_game, client_board):
            return {"error": "Некорректный ход! Изменение прошлых ходов запрещено, или сделано более одного хода."}, 400

        current_game.board = client_board

        is_over, winner = self._game_service.check_game_over(current_game.board)

        if not is_over:
            bot_player = 2  # Предположим: 1 - Игрок (X), 2 - Бот (O)
            bot_move = self._game_service.get_move(current_game, bot_player)

            if bot_move:
                row, col = bot_move
                current_game.board[row][col] = bot_player
                # Снова проверяем, не выиграл ли бот или не наступила ли ничья
                is_over, winner = self._game_service.check_game_over(current_game.board)

        self._game_repository.save_game(current_game)

        response_dto = WebMapper.to_dto(current_game, is_over=is_over, winner=winner)
        return response_dto.__dict__, 200
