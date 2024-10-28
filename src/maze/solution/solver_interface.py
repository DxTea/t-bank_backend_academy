from abc import ABC, abstractmethod


class ISolver(ABC):
    @abstractmethod
    def solve_maze(self, algorithm):
        """
        Решает лабиринт, используя указанный алгоритм.

        :param algorithm: Алгоритм,
        который будет использоваться для решения лабиринта.
        :return: Список координат,
        представляющих путь от начала до конца лабиринта.
        """
        pass
