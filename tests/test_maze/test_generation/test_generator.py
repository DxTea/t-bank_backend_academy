import unittest
from unittest.mock import MagicMock, patch
from src.maze.maze import Maze
from src.maze.generation.generator import Generator


class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.width = 10
        self.height = 10
        self.generator = Generator(self.width, self.height)

    def test_init(self):
        self.assertIsInstance(self.generator.maze, Maze)
        self.assertEqual(self.generator.maze.width, self.width)
        self.assertEqual(self.generator.maze.height, self.height)

    @patch('src.maze.algorithms.for_generation.g_kruskal.Kruskal.get_maze',
           return_value=MagicMock())
    def test_generate_maze_kruskal(self, mock_get_maze):
        result = self.generator.generate_maze("Краскал")
        self.assertTrue(mock_get_maze.called)
        self.assertEqual(result, mock_get_maze.return_value)

    @patch('src.maze.algorithms.for_generation.g_prim.Prim.get_maze',
           return_value=MagicMock())
    def test_generate_maze_prim(self, mock_get_maze):
        result = self.generator.generate_maze("Прим")
        self.assertTrue(mock_get_maze.called)
        self.assertEqual(result, mock_get_maze.return_value)

    @patch(
        'src.maze.algorithms.for_generation.g_recursive_backtracking'
        '.RecursiveBacktracking.get_maze',
        return_value=MagicMock())
    def test_generate_maze_recursive_backtracking(self, mock_get_maze):
        result = self.generator.generate_maze(
            "Рекурсивное обратное отслеживание")
        self.assertTrue(mock_get_maze.called)
        self.assertEqual(result, mock_get_maze.return_value)

    @patch(
        'src.maze.algorithms.for_generation.g_bin_tree.BinaryTreeMaze'
        '.get_maze',
        return_value=MagicMock())
    def test_generate_maze_binary_tree(self, mock_get_maze):
        result = self.generator.generate_maze("Двоичное дерево")
        self.assertTrue(mock_get_maze.called)
        self.assertEqual(result, mock_get_maze.return_value)

    def test_generate_maze_unknown_algorithm(self):
        with self.assertRaises(ValueError) as context:
            self.generator.generate_maze("Неизвестный алгоритм")
        self.assertEqual(str(context.exception),
                         "Неизвестный алгоритм: Неизвестный алгоритм")


if __name__ == '__main__':
    unittest.main()
