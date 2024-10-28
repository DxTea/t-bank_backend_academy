from src.maze.algorithms.for_solution.base_solver import BaseSolver
from typing import Dict, Tuple, Optional

from src.maze.maze import Maze


class FordBellman(BaseSolver):
    def __init__(self, maze: Maze) -> None:
        """
        Инициализирует объект алгоритма Форда-Беллмана для решения лабиринта.

        :param maze: Объект лабиринта, который нужно решить.
        """
        super().__init__(maze)
        self.distances: Dict[Tuple[int, int], float] = {}
        self.predecessors: Dict[
            Tuple[int, int], Optional[Tuple[int, int]]] = {}

        # Инициализация расстояний для всех вершин
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] in [' ', '🪙', '☠️']:
                    self.distances[(x, y)] = float('inf')
                    self.predecessors[(x, y)] = None
        self.distances[self.start] = 0

    def solve(self) -> bool:
        """
        Решает лабиринт, используя алгоритм Форда-Беллмана.

        :return: True, если путь найден, иначе False.
        """
        for _ in range(self.width * self.height - 1):
            for y in range(self.height):
                for x in range(self.width):
                    if self.maze[y][x] in [' ', '🪙', '☠️']:
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if (
                                    0 <= nx < self.width and 0 <= ny <
                                    self.height and
                                    self.maze[ny][nx] in [' ', '🪙', '☠️']):
                                self._relax((x, y), (nx, ny))

        if self._detect_negative_cycle():
            print("Обнаружен цикл отрицательного веса")
            return False

        if (self.finish in self.distances and self.distances[self.finish] !=
                float('inf')):
            self._mark_path()
            return True
        return False

    def _detect_negative_cycle(self) -> bool:
        """
        Проверяет наличие циклов отрицательного веса.

        :return: True, если цикл отрицательного веса обнаружен, иначе False.
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] in [' ', '🪙', '☠️']:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and \
                                self.maze[ny][nx] in [' ', '🪙', '☠️']:
                            if (self.distances[(x, y)] + self.get_cost(nx,
                                                                       ny) <
                                    self.distances[(nx, ny)]):
                                return True
        return False

    def _relax(self, u: Tuple[int, int], v: Tuple[int, int]) -> None:
        """
        Выполняет релаксацию ребра между двумя вершинами.

        :param u: Координаты начальной вершины.
        :param v: Координаты конечной вершины.
        """
        cost: int = self.get_cost(v[0], v[1])
        if self.distances[u] + cost < self.distances[v]:
            self.distances[v] = self.distances[u] + cost
            self.predecessors[v] = u

    def get_cost(self, x: int, y: int) -> int:
        """
        Возвращает стоимость перехода в указанную клетку.

        :param x: Координата x клетки.
        :param y: Координата y клетки.
        :return: Стоимость перехода в клетку.
        """
        surface = self.maze_obj.get_surface(x, y)
        if surface:
            if surface.symbol == '🪙':
                return 1
                # Устанавливаем стоимость 1 для монеты,
                # чтобы избежать отрицательных весов
            elif surface.symbol == '☠️':
                return 1 + 10  # Увеличиваем стоимость на 10 для ловушки
        return 5  # Базовая стоимость для обычной клетки

    def _mark_path(self, **kwargs) -> None:
        """
        Отмечает найденный путь в лабиринте.
        :param **kwargs:
        """
        x, y = self.finish
        while (x, y) != self.start:
            self.maze[y][x] = '1'
            if ((x, y) not in self.predecessors
                    or self.predecessors[
                        (x, y)] is None):
                raise ValueError(f"Предшественник для {(x, y)} не найден")
            x, y = self.predecessors[(x, y)]
        self.maze[self.start[1]][self.start[0]] = '1'
