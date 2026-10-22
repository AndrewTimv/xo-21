# Игровые роуты

from flask import Blueprint, request, jsonify
from web.module.game_controller import GameController

game_blueprint = Blueprint('game', __name__)

# Ссылка на контроллер будет внедрена при инициализации приложения в DI/main
game_controller: GameController = None


def init_routes(controller: GameController):
    """
    Инициализирует глобальную ссылку на контроллер для использования в роутах.
    """
    global game_controller
    game_controller = controller
    return game_blueprint


@game_blueprint.route('/game/<string:game_id>', methods=['POST'])
def play_turn(game_id):
    """
    Эндпоинт для отправки хода пользователя и получения ответа от ИИ.
    """
    data = request.get_json()

    if not data or 'board' not in data:
        return jsonify({"error": "В теле запроса должно быть передано игровое поле 'board'"}), 400

    client_board = data['board']

    # Передаем управление в контроллер
    response_data, status_code = game_controller.handle_player_move(game_id, client_board)
    return jsonify(response_data), status_code
