import unittest
from unittest.mock import MagicMock
from src.maze.maze import Maze
from src.maze.algorithms.for_generation.g_kruskal import Kruskal
from src.maze.algorithms.for_generation.g_prim import Prim
from src.maze.algorithms.for_generation.g_recursive_backtracking import \
    RecursiveBacktracking
from src.maze.algorithms.for_generation.g_bin_tree import BinaryTreeMaze


class TestMazeGeneration(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.get_maze.return_value = [['#'] * 10 for _ in range(10)]

    def test_unknown_algorithm(self):
        with self.assertRaises(ValueError) as context:
            self._get_generator("Неизвестный алгоритм")
        self.assertEqual(str(context.exception),
                         "Неизвестный алгоритм: Неизвестный алгоритм")

    def _get_generator(self, algorithm):
        if algorithm == "Краскал":
            generator = Kruskal(self.mock_maze)
        elif algorithm == "Прим":
            generator = Prim(self.mock_maze)
        elif algorithm == "Рекурсивное обратное отслеживание":
            generator = RecursiveBacktracking(self.mock_maze)
        elif algorithm == "Двоичное дерево":
            generator = BinaryTreeMaze(self.mock_maze)
        else:
            raise ValueError(f"Неизвестный алгоритм: {algorithm}")
        return generator.get_maze()


if __name__ == '__main__':
    unittest.main()
