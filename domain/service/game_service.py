# Сервисы игры
from datasource.repository.game_repository_interfaces import GameRepositoryInterface
from domain.model.game import Game, Board
from domain.service.game_service_interface import GameServiceInterface


class GameService(GameServiceInterface):
    """
    Реализация бизнес-логики
    """
    def __init__(self, repository: GameRepositoryInterface):
        self.repository = repository


    def validate_board(self, current_game: Game, new_board: Board) -> bool:
        # Размерность доски
        if len(new_board) != 3 or any(len(row) != 3 for row in new_board):
            return False

        # Проверяем разницу
        diff_count = 0
        for r in range(3):
            for c in range(3):
                old_val = current_game.board[r][c]
                new_val = new_board[r][c]

                if old_val != 0 and old_val != new_val:
                    return False

                if old_val == 0 and new_val != old_val:
                    diff_count += 1

        return diff_count == 1


    def check_game_over(self, board: Board) -> tuple[bool, int | None]:
        # Проверка строк и столбцов
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != 0:
                return True, board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != 0:
                return True, board[0][i]

        # Проверка диагоналей
        if board[0][0] == board[1][1] == board[2][2] != 0:
            return True, board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != 0:
            return True, board[0][2]

        # Проверка на ничью (нет пустых клеток)
        if all(cell != 0 for row in board for cell in row):
            return True, 0  # 0 означает ничью

        return False, None

    def get_move(self, game: Game, bot_player: int) -> tuple[int, int] | None:
        is_over, _ = self.check_game_over(game.board)
        if is_over:
            return None

        best_score = float('-inf')
        best_move = None
        human_player = 1 if bot_player == 2 else 2

        for r in range(3):
            for c in range(3):
                if game.board[r][c] == 0:
                    game.board[r][c] = bot_player
                    score = self._minimax(game.board, 0, False, bot_player, human_player)
                    game.board[r][c] = 0  # Откат хода

                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        return best_move

    def _minimax(self, board: Board, depth: int, is_maximizing: bool, bot: int, human: int) -> int:
        is_over, winner = self.check_game_over(board)
        if is_over:
            if winner == bot: return 10 - depth
            if winner == human: return depth - 10
            return 0  # Ничья

        if is_maximizing:
            best_score = float('-inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == 0:
                        board[r][c] = bot
                        score = self._minimax(board, depth + 1, False, bot, human)
                        board[r][c] = 0
                        best_score = max(score, best_score)
            return int(best_score)
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == 0:
                        board[r][c] = human
                        score = self._minimax(board, depth + 1, True, bot, human)
                        board[r][c] = 0
                        best_score = min(score, best_score)
            return int(best_score)