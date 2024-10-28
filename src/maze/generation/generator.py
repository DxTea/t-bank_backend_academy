from src.maze.generation.generator_interface import IGenerator
from src.maze.algorithms.for_generation.g_kruskal import Kruskal
from src.maze.algorithms.for_generation.g_prim import Prim
from src.maze.algorithms.for_generation.g_recursive_backtracking import \
    RecursiveBacktracking
from src.maze.algorithms.for_generation.g_bin_tree import BinaryTreeMaze
from src.maze.maze import Maze
from typing import List


class Generator(IGenerator):
    def __init__(self, width: int, height: int) -> None:
        """
        Инициализирует объект генератора лабиринта с заданными размерами.

        :param width: Ширина лабиринта
        :param height: Высота лабиринта
        """
        self.maze = Maze(width, height)

    def generate_maze(self, algorithm: str) -> List[List[str]]:
        """
        Генерирует лабиринт, используя указанный алгоритм.

        :param algorithm: Алгоритм, который будет использоваться для
        генерации лабиринта.
        :return: Сгенерированный лабиринт.
        :raises ValueError: Если указанный алгоритм неизвестен.
        """
        if algorithm == "Краскал":
            generator = Kruskal(self.maze)
        elif algorithm == "Прим":
            generator = Prim(self.maze)
        elif algorithm == "Рекурсивное обратное отслеживание":
            generator = RecursiveBacktracking(self.maze)
        elif algorithm == "Двоичное дерево":
            generator = BinaryTreeMaze(self.maze)
        else:
            raise ValueError(f"Неизвестный алгоритм: {algorithm}")

        return generator.get_maze()
