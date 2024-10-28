from abc import ABC, abstractmethod
from typing import Any


class IGenerator(ABC):
    @abstractmethod
    def generate_maze(self, algorithm: str) -> Any:
        """
        Генерирует лабиринт, используя указанный алгоритм.

        :param algorithm: Алгоритм, который будет использоваться для
        генерации лабиринта.
        :return: Сгенерированный лабиринт.
        """
        pass
