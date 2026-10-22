# Точка входа в приложение

from flask import Flask, jsonify
from di.container import Container
from web.route.game_routes import init_routes
from domain.model.game import Game

def create_app() -> Flask:
    app = Flask(__name__)

    # Инициализируем граф зависимостей через контейнер
    container = Container()

    # Получаем контроллер и регистрируем роуты веб-слоя
    controller = container.get_game_controller()
    blueprint = init_routes(controller)
    app.register_blueprint(blueprint)

    # Получаем репозиторий для возможности создавать новые игры на старте
    repository = container.get_game_repository()

    @app.route('/game', methods=['POST'])
    def create_game():
        """Вспомогательный эндпоинт для инициализации новой игры и получения UUID."""
        new_game = Game()  # Генерирует новый UUID и пустое поле 3x3
        repository.save_game(new_game)
        return jsonify({
            "game_id": str(new_game.id),
            "board": new_game.board
        }), 201

    return app

if __name__ == '__main__':
    app = create_app()
    # Запуск сервера на порту 5000
    app.run(debug=True, port=5000)
