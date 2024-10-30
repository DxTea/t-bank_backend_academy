import unittest
from unittest.mock import MagicMock, patch
from src.maze.maze import Maze
from src.maze.algorithms.for_generation.g_bin_tree import BinaryTreeMaze


class TestBinaryTreeMaze(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.get_width.return_value = 10
        self.mock_maze.get_height.return_value = 10
        self.mock_maze.get_maze.return_value = [['#'] * 10 for _ in range(10)]
        self.generator = BinaryTreeMaze(self.mock_maze)

    @patch('src.maze.algorithms.for_generation.g_bin_tree.random.choice')
    def test_generate_maze(self, mock_random_choice):
        mock_random_choice.side_effect = lambda neighbors: neighbors[0]
        self.generator._generate_maze()
        self.assertEqual(self.generator.maze[0][0], ' ')
        self.assertEqual(self.generator.maze[0][1], ' ')
        self.assertEqual(self.generator.maze[1][0], ' ')

    def test_set_exit(self):
        self.generator._set_exit()
        self.assertEqual(self.generator.maze[9][9], ' ')

    def test_get_maze(self):
        maze = self.generator.get_maze()
        self.assertEqual(maze, self.mock_maze)
        self.assertEqual(maze.maze, self.generator.maze)


if __name__ == '__main__':
    unittest.main()
