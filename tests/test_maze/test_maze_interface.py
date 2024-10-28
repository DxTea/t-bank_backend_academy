
import unittest
from src.maze.maze_interface import IMaze


class MockMaze(IMaze):
    def get_width(self) -> int:
        return 10

    def get_height(self) -> int:
        return 10

    def get_maze(self):
        return [['#'] * 10 for _ in range(10)]


class TestIMaze(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MockMaze()

    def test_get_width(self):
        self.assertEqual(self.mock_maze.get_width(), 10)

    def test_get_height(self):
        self.assertEqual(self.mock_maze.get_height(), 10)

    def test_get_maze(self):
        maze = self.mock_maze.get_maze()
        self.assertEqual(len(maze), 10)
        self.assertEqual(len(maze[0]), 10)
        self.assertEqual(maze[0][0], '#')


if __name__ == '__main__':
    unittest.main()
