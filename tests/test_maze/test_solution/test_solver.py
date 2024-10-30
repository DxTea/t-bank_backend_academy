import unittest
from unittest.mock import MagicMock, patch
from src.maze.solution.solver import Solver
from src.maze.maze import Maze
from src.maze.algorithms.for_solution.s_a_star import AStar


class TestSolver(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.start = (0, 0)
        self.mock_maze.finish = (1, 1)
        self.mock_maze.width = 10
        self.mock_maze.height = 10
        self.mock_algorithm = MagicMock(spec=AStar)
        self.solver = Solver("A*", self.mock_maze)
        self.solver.algorithm_instance = self.mock_algorithm

    def test_initialization(self):
        self.assertEqual(self.solver.maze, self.mock_maze)

    @patch('src.maze.algorithms.for_solution.s_a_star.AStar.solve',
           return_value=True)
    def test_solve_a_star(self, mock_solve):
        solver = Solver("A*", self.mock_maze)
        result = solver.solve()
        self.assertTrue(result)
        mock_solve.assert_called_once()

    @patch('src.maze.algorithms.for_solution.s_bfs.BFS.solve',
           return_value=True)
    def test_solve_bfs(self, mock_solve):
        solver = Solver("BFS", self.mock_maze)
        result = solver.solve()
        self.assertTrue(result)
        mock_solve.assert_called_once()

    @patch('src.maze.algorithms.for_solution.s_dfs.DFS.solve',
           return_value=True)
    def test_solve_dfs(self, mock_solve):
        solver = Solver("DFS", self.mock_maze)
        result = solver.solve()
        self.assertTrue(result)
        mock_solve.assert_called_once()

    @patch('src.maze.algorithms.for_solution.s_ford_bellman.FordBellman.solve',
           return_value=True)
    def test_solve_ford_bellman(self, mock_solve):
        solver = Solver("Форд-Беллман", self.mock_maze)
        result = solver.solve()
        self.assertTrue(result)
        mock_solve.assert_called_once()

    def test_solve_unknown_algorithm(self):
        solver = Solver("Unknown", self.mock_maze)
        with self.assertRaises(ValueError) as context:
            solver.solve()
        self.assertEqual(str(context.exception),
                         "Неизвестный алгоритм: Unknown")


if __name__ == '__main__':
    unittest.main()
