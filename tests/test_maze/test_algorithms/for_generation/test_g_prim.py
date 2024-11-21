import unittest
from unittest.mock import MagicMock, patch
from src.maze.maze import Maze
from src.maze.algorithms.for_generation.g_prim import Prim


class TestPrim(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.start = (0, 0)
        self.mock_maze.finish = (9, 9)
        self.mock_maze.get_width.return_value = 10
        self.mock_maze.get_height.return_value = 10
        self.mock_maze.get_maze.return_value = [['#'] * 10 for _ in range(10)]
        self.generator = Prim(self.mock_maze)

    @patch('src.maze.algorithms.for_generation.g_prim.random.choice')
    def test_generate_maze_prim(self, mock_random_choice):
        mock_random_choice.side_effect = lambda frontier: frontier[0]
        self.generator._generate_maze_prim()
        self.assertEqual(self.generator.maze[0][0], ' ')
        self.assertIn(' ', [self.generator.maze[y][x] for x, y in
                            self.generator._get_neighbors(0, 0)])

    def test_get_neighbors(self):
        neighbors = self.generator._get_neighbors(0, 0)
        self.assertIn((1, 0), neighbors)
        self.assertIn((0, 1), neighbors)
        self.assertNotIn((-1, 0), neighbors)
        self.assertNotIn((0, -1), neighbors)

    def test_set_exit(self):
        self.generator._set_exit()
        self.assertEqual(self.generator.maze[9][9], ' ')

    def test_get_maze(self):
        maze = self.generator.get_maze()
        self.assertEqual(maze, self.mock_maze)
        self.assertEqual(maze.maze, self.generator.maze)


if __name__ == '__main__':
    unittest.main()
