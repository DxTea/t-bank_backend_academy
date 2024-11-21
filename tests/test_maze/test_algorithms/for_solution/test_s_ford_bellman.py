import unittest
from src.maze.algorithms.for_solution.s_ford_bellman import FordBellman
from src.maze.maze import Maze


class TestFordBellman(unittest.TestCase):

    def setUp(self):
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
        self.solver = FordBellman(self.maze)

    def test_initialization(self):
        self.assertEqual(self.solver.distances[(0, 0)], 0)
        self.assertEqual(self.solver.distances[(3, 3)], float('inf'))
        self.assertIsNone(self.solver.predecessors[(0, 0)])
        self.assertIsNone(self.solver.predecessors[(3, 3)])

    def test_solve(self):
        result = self.solver.solve()
        self.assertTrue(result)
        self.assertEqual(self.solver.distances[self.solver.finish],
                         30)

    def test_detect_negative_cycle(self):
        self.solver.distances[(1, 1)] = -1
        self.solver.predecessors[(1, 1)] = (0, 0)
        self.solver.distances[(2, 1)] = -2
        self.solver.predecessors[(2, 1)] = (1, 1)
        self.solver.distances[(1, 2)] = -3
        self.solver.predecessors[(1, 2)] = (2, 1)
        self.solver.distances[(0, 1)] = -4
        self.solver.predecessors[(0, 1)] = (1, 2)
        self.solver.distances[(0, 0)] = -5
        self.solver.predecessors[(0, 0)] = (0, 1)
        self.assertTrue(self.solver._detect_negative_cycle())


if __name__ == '__main__':
    unittest.main()
