from abc import abstractmethod
from typing import List, Tuple, Protocol


class ISolver(Protocol):
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
