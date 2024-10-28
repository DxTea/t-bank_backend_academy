from abc import ABC, abstractmethod
from typing import List, Tuple


class ISolver(ABC):
    @abstractmethod
    def solve_maze(self, algorithm: str) -> List[Tuple[int, int]]:
        """
        Решает лабиринт, используя указанный алгоритм.

        :param algorithm: Алгоритм,
        который будет использоваться для решения лабиринта.
        :return: Список координат,
        представляющих путь от начала до конца лабиринта.
        """
        pass
