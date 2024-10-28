# tests/test_maze/test_solution/test_solver.py

import unittest
from unittest.mock import MagicMock
from src.maze.solution.solver import Solver
from src.maze.maze import Maze
from src.maze.algorithms.for_solution.s_a_star import AStar


class TestSolver(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.start = (0, 0)  # Set the start attribute
        self.mock_maze.finish = (1, 1)  # Set the finish attribute
        self.mock_maze.width = 10  # Set the width attribute
        self.mock_maze.height = 10  # Set the height attribute
        self.mock_algorithm = MagicMock(spec=AStar)
        self.solver = Solver("A*", self.mock_maze)
        self.solver.algorithm_instance = self.mock_algorithm

    def test_initialization(self):
        self.assertEqual(self.solver.maze, self.mock_maze)


if __name__ == '__main__':
    unittest.main()
