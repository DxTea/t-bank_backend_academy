from abc import abstractmethod
from typing import Any, Protocol


class IGenerator(Protocol):
    @abstractmethod
    def generate_maze(self, algorithm: str) -> Any:
        """
        Генерирует лабиринт, используя указанный алгоритм.

        :param algorithm: Алгоритм, который будет использоваться для
        генерации лабиринта.
        :return: Сгенерированный лабиринт.
        """
        pass
