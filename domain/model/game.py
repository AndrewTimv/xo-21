# Модель игры

import uuid
from dataclasses import dataclass, field


class Figures:
    EMPTY = 0
    X = 1
    O = 2


Board = list[list[int]]


@dataclass
class Game:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    board: Board = field(default_factory=lambda: [[0, 0, 0] for _ in range(3)])
