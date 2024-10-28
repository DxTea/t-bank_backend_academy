from typing import Dict, Tuple, List, Set

from src.maze.maze import Maze


class BaseSolver:
    def __init__(self, maze: Maze) -> None:
        """
        Инициализирует базовый объект алгоритма для решения лабиринта.

        :param maze: Объект лабиринта, который нужно решить.
        """
        self.maze_obj = maze
        self.width = maze.get_width()
        self.height: int = maze.get_height()
        self.maze: List[List[str]] = maze.get_maze()
        self.start: Tuple[int, int] = maze.start
        self.finish: Tuple[int, int] = maze.finish
        self.g_score: Dict[Tuple[int, int], int] = {}

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
                return 1 - 5  # Уменьшаем стоимость на 5 для монеты
            elif surface.symbol == '☠️':
                return 1 + 10  # Увеличиваем стоимость на 10 для ловушки
        return 1  # Базовая стоимость для обычной клетки

    def _mark_path(self,
                   parent: Dict[Tuple[int, int], Tuple[int, int]]) -> None:
        """
        Отмечает найденный путь в лабиринте.

        :param parent: Словарь, содержащий предшественников для каждой клетки.
        """
        x, y = self.finish
        while (x, y) != self.start:
            self.maze[y][x] = '1'
            x, y = parent[(x, y)]
        self.maze[self.start[1]][self.start[0]] = '1'

    def get_maze(self):
        """
        Возвращает объект лабиринта.

        :return: Объект Maze.
        """
        return self.maze_obj

    def _process_current_node(self, current: Tuple[int, int],
                              parent: Dict[Tuple[int, int], Tuple[int, int]],
                              visited: Set[Tuple[int, int]],
                              container) -> bool:
        """
        Обрабатывает текущую клетку в процессе поиска пути.

        :param current: Текущая клетка.
        :param parent: Словарь, содержащий предшественников для каждой клетки.
        :param visited: Множество посещенных клеток.
        :param container: Контейнер для хранения клеток, подлежащих
        обработке (очередь или стек).
        :return: True, если путь найден, иначе False.
        """
        if current == self.finish:
            self._mark_path(parent)
            return True

        visited.add(current)
        x, y = current

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor: Tuple[int, int] = (x + dx, y + dy)
            if (0 <= neighbor[0] < self.width and 0 <= neighbor[1] <
                    self.height):
                if neighbor in visited:
                    continue
                if self.maze[neighbor[1]][neighbor[0]] in [' ', '🪙', '☠️']:
                    tentative_g_score: int = self.g_score[
                                                 current] + self.get_cost(
                        neighbor[0], neighbor[1])
                    if neighbor not in self.g_score or tentative_g_score < \
                            self.g_score[neighbor]:
                        parent[neighbor] = current
                        self.g_score[neighbor] = tentative_g_score
                        container.append(neighbor)
        return False
