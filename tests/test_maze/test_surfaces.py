import unittest
from src.maze.maze import Maze, Trap


class TestSurfaces(unittest.TestCase):

    def setUp(self):
        self.maze = Maze(3, 3)

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


if __name__ == '__main__':
    unittest.main()
