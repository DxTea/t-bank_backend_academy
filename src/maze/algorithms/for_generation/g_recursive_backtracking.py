import random

from typing import List, Tuple
from src.maze.algorithms.for_generation.base_maze_generator import \
    BaseMazeGenerator


class RecursiveBacktracking(BaseMazeGenerator):
    def __init__(self, maze) -> None:
        """
        Инициализирует объект алгоритма рекурсивного поиска в глубину для
        генерации лабиринта.

        :param maze: Объект лабиринта, который нужно сгенерировать.
        """
        super().__init__(maze)
        self._generate_maze()
        self._set_exit()

    def _generate_maze(self) -> None:
        """
        Генерирует лабиринт, начиная с верхнего левого угла.
        """
        start_x, start_y = 0, 0
        self.maze[start_y][start_x] = ' '
        self._carve_passages_from(start_x, start_y)

    def _carve_passages_from(self, cx: int, cy: int) -> None:
        """
        Рекурсивно создает проходы в лабиринте, начиная с заданной клетки.

        :param cx: Координата x текущей клетки.
        :param cy: Координата y текущей клетки.
        """
        directions: List[Tuple[int, int]] = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.maze[ny][nx] == '#':
                    self.maze[cy + dy // 2][cx + dx // 2] = ' '
                    self.maze[ny][nx] = ' '
                    self._carve_passages_from(nx, ny)
