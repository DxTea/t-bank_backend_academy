import unittest
from unittest.mock import MagicMock, patch
from src.maze.maze import Maze
from src.maze.algorithms.for_generation.g_kruskal import Kruskal


class TestKruskal(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.get_width.return_value = 10
        self.mock_maze.get_height.return_value = 10
        self.mock_maze.get_maze.return_value = [['#'] * 10 for _ in range(10)]
        self.generator = Kruskal(self.mock_maze)

    def test_initialize_maze(self):
        self.generator._initialize_maze()
        self.assertEqual(self.generator.maze[0][0], ' ')
        self.assertIn(((0, 0), (2, 0)), self.generator.edges)
        self.assertIn(((0, 0), (0, 2)), self.generator.edges)

    def test_find(self):
        self.generator.parent = {(0, 0): (0, 0), (2, 0): (0, 0)}
        root = self.generator._find((2, 0))
        self.assertEqual(root, (0, 0))

    def test_union(self):
        self.generator.parent = {(0, 0): (0, 0), (2, 0): (2, 0)}
        self.generator.rank = {(0, 0): 0, (2, 0): 0}
        self.generator._union((0, 0), (2, 0))
        self.assertEqual(self.generator._find((0, 0)),
                         self.generator._find((2, 0)))

    @patch('src.maze.algorithms.for_generation.g_kruskal.random.shuffle')
    def test_generate_maze_kruskal(self, mock_shuffle):
        # Ensure the shuffle function does not change the order of elements
        mock_shuffle.side_effect = lambda x: x.sort()
        self.generator._generate_maze_kruskal()
        self.assertEqual(self.generator.maze[0][0], ' ')
        self.assertEqual(self.generator.maze[2][0], ' ')
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
