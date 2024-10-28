from src.maze.generation.generator_interface import IGenerator
from src.maze.algorithms.for_generation.g_kruskal import Kruskal
from src.maze.algorithms.for_generation.g_prim import Prim
from src.maze.algorithms.for_generation.g_recursive_backtracking import \
    RecursiveBacktracking
from src.maze.algorithms.for_generation.g_bin_tree import BinaryTreeMaze
from src.maze.maze import Maze


class Generator(IGenerator):
    def __init__(self, width, height):
        """
        Инициализирует объект генератора лабиринта с заданными размерами.

        :param width: Ширина лабиринта
        :param height: Высота лабиринта
        :return: Объект Maze с заданными параметрами.
        """
        self.maze = Maze(width, height)

    def generate_maze(self, algorithm):
        """
        Генерирует лабиринт, используя указанный алгоритм.

        :param algorithm: Алгоритм, который будет использоваться для генерации лабиринта.
        :return: Сгенерированный лабиринт.
        :raises ValueError: Если указанный алгоритм неизвестен.
        """

        if algorithm == "Kruskal":
            generator = Kruskal(self.maze)
        elif algorithm == "Prim":
            generator = Prim(self.maze)
        elif algorithm == "Recursive Backtracking":
            generator = RecursiveBacktracking(self.maze)
        elif algorithm == "Binary Tree":
            generator = BinaryTreeMaze(self.maze)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        return generator.get_maze()
