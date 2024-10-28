import unittest
from src.maze.algorithms.for_solution.s_dfs import DFS
from src.maze.maze import Maze


class TestDFS(unittest.TestCase):

    def setUp(self):
        # Create a simple maze for testing
        self.maze_data = [
            [' ', ' ', ' ', ' '],
            [' ', '☠️', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ']
        ]
        self.maze = Maze(4, 4)
        self.maze.maze = self.maze_data
        self.maze.start = (0, 0)
        self.maze.finish = (3, 3)
        self.solver = DFS(self.maze)
        self.solver.g_score = {pos: float('inf') for row in
                               range(self.maze.height) for pos in
                               [(row, col) for col in range(self.maze.width)]}
        self.solver.g_score[self.maze.start] = 0

    def test_initialization(self):
        self.assertEqual(self.solver.g_score[self.maze.start], 0)
        self.assertEqual(self.solver.g_score[self.maze.finish], float('inf'))

    def test_solve(self):
        result = self.solver.solve()
        self.assertTrue(result)
        self.assertEqual(self.solver.g_score[self.maze.finish], 6)


if __name__ == '__main__':
    unittest.main()
