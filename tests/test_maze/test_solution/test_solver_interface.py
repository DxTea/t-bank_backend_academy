# tests/test_maze/test_solution/test_solver_interface.py

import unittest
from unittest.mock import MagicMock

from src.maze.solution.solver_interface import ISolver


class MockSolver(ISolver):
    def solve(self, maze):
        return True

    def solve_maze(self, maze):
        return True


class TestISolver(unittest.TestCase):

    def setUp(self):
        self.mock_solver = MockSolver()
        self.mock_maze = MagicMock()

    def test_solve(self):
        result = self.mock_solver.solve(self.mock_maze)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
