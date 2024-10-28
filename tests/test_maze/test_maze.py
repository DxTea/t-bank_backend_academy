# tests/test_maze/test_maze.py

import unittest
from unittest.mock import MagicMock
from src.maze.maze import Maze, Trap


class TestMaze(unittest.TestCase):

    def setUp(self):
        self.maze = Maze(3, 3)
        self.maze.reset = MagicMock()

    def test_initialization(self):
        self.assertEqual(self.maze.width, 3)
        self.assertEqual(self.maze.height, 3)
        self.assertEqual(len(self.maze.maze), 3)
        self.assertEqual(len(self.maze.maze[0]), 3)

    def test_set_surface(self):
        trap = Trap()
        self.maze.set_surface(1, 1, trap)
        self.assertEqual(self.maze.get_surface(1, 1), trap)
        self.assertEqual(self.maze.maze[1][1], trap.symbol)

        self.maze.set_surface(1, 1, None)
        self.assertIsNone(self.maze.get_surface(1, 1))
        self.assertEqual(self.maze.maze[1][1], ' ')

    def test_get_surface(self):
        trap = Trap()
        self.maze.set_surface(1, 1, trap)
        self.assertEqual(self.maze.get_surface(1, 1), trap)
        self.assertIsNone(self.maze.get_surface(0, 0))

    def test_reset(self):
        self.maze.reset()
        self.maze.reset.assert_called_once()


if __name__ == '__main__':
    unittest.main()
