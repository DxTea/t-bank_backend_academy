import unittest
from unittest.mock import MagicMock, patch
from src.maze.maze import Maze, Trap


class TestMaze(unittest.TestCase):

    def setUp(self):
        self.maze = Maze(3, 3)
        self.maze.reset = MagicMock()

    def test_initialization(self):
        self.assertEqual(self.maze.width, 3)
        self.assertEqual(self.maze.height, 3)
        self.assertEqual(len(self.maze.maze), 3)
        self.assertEqual(len(self.maze.maze[0]), 3)

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

    def test_reset(self):
        self.maze.reset()
        self.maze.reset.assert_called_once()

    @patch('random.shuffle')
    def test_place_random_surfaces(self, mock_shuffle):
        self.maze.set_surface = MagicMock()
        mock_shuffle.side_effect = lambda x: x

        self.maze.maze = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]

        self.maze.place_random_surfaces(num_traps=2, num_coins=1)

        expected_calls = [
            unittest.mock.call(1, 2, unittest.mock.ANY),
            unittest.mock.call(0, 2, unittest.mock.ANY),
            unittest.mock.call(2, 2, unittest.mock.ANY)
        ]
        self.maze.set_surface.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(self.maze.set_surface.call_count, 3)


if __name__ == '__main__':
    unittest.main()
