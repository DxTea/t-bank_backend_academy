import random

from src.maze.algorithms.for_generation.base_maze_generator import \
    BaseMazeGenerator


class Prim(BaseMazeGenerator):
    def __init__(self, maze):
        """
        Инициализирует объект алгоритма Прима для генерации лабиринта.

        :param maze: Объект лабиринта, который нужно сгенерировать.
        """
        super().__init__(maze)
        self.start = maze.start
        self.finish = maze.finish
        self._generate_maze_prim()
        self._set_exit()

    def _generate_maze_prim(self):
        """
        Генерирует лабиринт, используя алгоритм Прима.
        """
        start_x, start_y = self.start
        self.maze[start_y][start_x] = ' '
        frontier = self._get_neighbors(start_x, start_y)

        while frontier:
            x, y = random.choice(frontier)
            frontier.remove((x, y))

            if self._is_valid_frontier(x, y):
                self.maze[y][x] = ' '
                for nx, ny in self._get_neighbors(x, y):
                    if self.maze[ny][nx] == '#':
                        frontier.append((nx, ny))

    def _is_valid_frontier(self, x, y):
        """
        Проверяет, является ли указанная клетка допустимой границей.

        :param x: Координата x клетки.
        :param y: Координата y клетки.
        :return: True, если клетка является допустимой границей, иначе False.
        """
        neighbors = self._get_neighbors(x, y)
        valid_neighbors = sum(
            1 for nx, ny in neighbors if self.maze[ny][nx] == ' ')
        return valid_neighbors == 1

    def _get_neighbors(self, x, y, step=1):
        """
        Возвращает список соседних клеток для указанной клетки.

        :param x: Координата x клетки.
        :param y: Координата y клетки.
        :param step: Шаг для определения соседних клеток.
        :return: Список координат соседних клеток.
        """
        neighbors = []
        for dx, dy in [(-step, 0), (step, 0), (0, -step), (0, step)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors
