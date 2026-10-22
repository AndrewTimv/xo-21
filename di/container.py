# Конфигурация di-контейнера

from datasource.repository.storage import InMemoryStorage
from datasource.repository.game_repository import GameRepository
from domain.service.game_service import GameService
from web.module.game_controller import GameController

class Container:
    """Контейнер для управления и внедрения зависимостей (Dependency Injection)."""

    def __init__(self):
        # 1. Хранилище как singleton (InMemoryStorage сам по себе реализован как синглтон)
        self._storage = InMemoryStorage()

        # 2. Репозиторий для работы с классом-хранилищем
        self._repository = GameRepository(storage=self._storage)

        # 3. Сервис для работы с бизнес-логикой и репозиторием
        self._game_service = GameService(repository=self._repository)

        # 4. Веб-контроллер, собирающий сервис и репозиторий
        self._game_controller = GameController(
            game_service=self._game_service,
            game_repository=self._repository
        )

    def get_game_repository(self) -> GameRepository:
        return self._repository

    def get_game_service(self) -> GameService:
        return self._game_service

    def get_game_controller(self) -> GameController:
        return self._game_controller
