import random

from src.maze.algorithms.for_generation.base_maze_generator import \
    BaseMazeGenerator


class BinaryTreeMaze(BaseMazeGenerator):
    def __init__(self, maze):
        """
        Инициализирует объект алгоритма генерации лабиринта с
        использованием бинарного дерева.

        :param maze: Объект лабиринта, который нужно сгенерировать.
        """
        super().__init__(maze)
        self._initialize_maze()
        self._generate_maze()
        self._set_exit()

    def _initialize_maze(self):
        """
        Инициализирует лабиринт, заполняя его стенами.
        """
        for y in range(self.height):
            for x in range(self.width):
                self.maze[y][x] = '#'

    def _generate_maze(self):
        """
        Генерирует лабиринт, используя алгоритм бинарного дерева.
        """
        for y in range(0, self.height, 2):
            for x in range(0, self.width, 2):
                self.maze[y][x] = ' '
                neighbors = []
                if x > 0:
                    neighbors.append((x - 1, y))
                if y > 0:
                    neighbors.append((x, y - 1))
                if neighbors:
                    nx, ny = random.choice(neighbors)
                    self.maze[ny][nx] = ' '
