# tests/test_maze/test_algorithms/for_solution/test_base_solver.py

import unittest
from unittest.mock import MagicMock
from src.maze.maze import Maze
from src.maze.algorithms.for_solution.base_solver import BaseSolver


class TestBaseSolver(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.start = (0, 0)
        self.mock_maze.finish = (1, 1)
        self.mock_maze.get_width.return_value = 10
        self.mock_maze.get_height.return_value = 10
        self.mock_maze.get_maze.return_value = [[' '] * 10 for _ in range(10)]
        self.mock_maze.get_surface.return_value = None
        self.solver = BaseSolver(self.mock_maze)

    def test_initialization(self):
        self.assertEqual(self.solver.width, 10)
        self.assertEqual(self.solver.height, 10)
        self.assertEqual(self.solver.start, (0, 0))
        self.assertEqual(self.solver.finish, (1, 1))

    def test_get_cost_default(self):
        self.mock_maze.get_surface.return_value = None
        cost = self.solver.get_cost(0, 0)
        self.assertEqual(cost, 1)

    def test_get_cost_coin(self):
        surface = MagicMock()
        surface.symbol = '🪙'
        self.mock_maze.get_surface.return_value = surface
        cost = self.solver.get_cost(0, 0)
        self.assertEqual(cost, -4)

    def test_get_cost_trap(self):
        surface = MagicMock()
        surface.symbol = '☠️'
        self.mock_maze.get_surface.return_value = surface
        cost = self.solver.get_cost(0, 0)
        self.assertEqual(cost, 11)

    def test_mark_path(self):
        parent = {(1, 1): (0, 1), (0, 1): (0, 0)}
        self.solver._mark_path(parent)
        self.assertEqual(self.solver.maze[0][0], '1')
        self.assertEqual(self.solver.maze[1][0], '1')
        self.assertEqual(self.solver.maze[1][1], '1')

    def test_get_maze(self):
        maze = self.solver.get_maze()
        self.assertEqual(maze, self.mock_maze)


if __name__ == '__main__':
    unittest.main()
