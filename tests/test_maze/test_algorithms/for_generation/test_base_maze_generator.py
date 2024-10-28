# tests/test_maze/test_algorithms/for_generation/test_base_maze_generator.py

import unittest
from unittest.mock import MagicMock
from src.maze.maze import Maze
from src.maze.algorithms.for_generation.base_maze_generator import \
    BaseMazeGenerator


class TestBaseMazeGenerator(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.get_width.return_value = 10
        self.mock_maze.get_height.return_value = 10
        self.mock_maze.get_maze.return_value = [['#'] * 10 for _ in range(10)]
        self.generator = BaseMazeGenerator(self.mock_maze)

    def test_initialization(self):
        self.assertEqual(self.generator.width, 10)
        self.assertEqual(self.generator.height, 10)
        self.assertEqual(self.generator.maze, [['#'] * 10 for _ in range(10)])

    def test_set_exit_even_width(self):
        self.generator.width = 10
        self.generator._set_exit()
        self.assertEqual(self.generator.maze[9][9], ' ')

    def test_set_exit_odd_width(self):
        self.generator.width = 9
        self.generator._set_exit()
        self.assertEqual(self.generator.maze[9][8], ' ')

    def test_get_maze(self):
        maze = self.generator.get_maze()
        self.assertEqual(maze, self.mock_maze)
        self.assertEqual(maze.maze, self.generator.maze)


if __name__ == '__main__':
    unittest.main()
