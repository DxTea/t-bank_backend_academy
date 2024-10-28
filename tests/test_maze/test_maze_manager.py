import unittest
from unittest.mock import MagicMock
from src.maze.maze_manager import MazeManager
from src.maze.maze import Maze


class TestMazeManager(unittest.TestCase):

    def setUp(self):
        self.maze = MagicMock(spec=Maze)
        self.maze_manager = MagicMock(spec=MazeManager)
        self.maze_manager.maze = self.maze
        self.maze_manager.generate_maze = MagicMock()
        self.maze_manager.solve_maze = MagicMock()
        self.maze_manager.reset_maze = MagicMock()

    def test_initialization(self):
        self.assertEqual(self.maze_manager.maze, self.maze)

    def test_generate_maze(self):
        self.maze_manager.generate_maze(3, "Прим", "Краскал")
        self.maze_manager.generate_maze.assert_called_once_with(3, "Прим",
                                                                "Краскал")

    def test_solve_maze(self):
        self.maze_manager.solve_maze("A*")
        self.maze_manager.solve_maze.assert_called_once_with("A*")

    def test_reset_maze(self):
        self.maze_manager.reset_maze()
        self.maze_manager.reset_maze.assert_called_once()


if __name__ == '__main__':
    unittest.main()
