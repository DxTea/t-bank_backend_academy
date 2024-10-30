import unittest
from unittest.mock import MagicMock
from src.maze.algorithms.for_solution.s_a_star import AStar
from src.maze.maze import Maze


class TestAStar(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.get_maze.return_value = [[' ' for _ in range(5)] for _
                                                in range(5)]
        self.mock_maze.start = (0, 0)
        self.mock_maze.finish = (4, 4)
        self.mock_maze.get_cost = MagicMock(
            return_value=1)
        self.astar = AStar(self.mock_maze)
        self.astar.width = 5
        self.astar.height = 5

    def test_initialization(self):
        self.assertEqual(self.astar.start, (0, 0))
        self.assertEqual(self.astar.finish, (4, 4))
        self.assertIn((self.astar.f_score[self.astar.start], self.astar.start),
                      self.astar.open_set)

    def test_heuristic(self):
        self.mock_maze.get_surface.return_value = None
        heuristic = self.astar._heuristic((0, 0), (4, 4))
        self.assertEqual(heuristic, 8)

    def test_mark_path(self):
        self.astar.came_from = {(4, 4): (3, 4), (3, 4): (2, 4), (2, 4): (1, 4),
                                (1, 4): (0, 4), (0, 4): (0, 3), (0, 3): (0, 2),
                                (0, 2): (0, 1), (0, 1): (0, 0)}
        self.astar._mark_path((4, 4))
        self.assertEqual(self.astar.maze[4][4], '1')
        self.assertEqual(self.astar.maze[0][0], '1')

    def test_solve(self):
        self.mock_maze.get_surface.return_value = None
        self.assertTrue(self.astar.solve())
        self.assertIn((4, 3), self.astar.visited)


if __name__ == '__main__':
    unittest.main()
