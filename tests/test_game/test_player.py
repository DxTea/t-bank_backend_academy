import unittest
from src.game.player import Player
from unittest.mock import MagicMock


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.start_position = (0, 0)
        self.player = Player(self.start_position)
        self.mock_maze = [[' ' for _ in range(5)] for _ in range(5)]
        self.mock_maze_obj = MagicMock()

    def test_initialization(self):
        self.assertEqual(self.player.position, self.start_position)
        self.assertEqual(self.player.score, 0)

    def test_move_up(self):
        self.mock_maze[1][0] = ' '
        self.player.move('w', self.mock_maze, self.mock_maze_obj)
        self.assertEqual(self.player.position, (0, 0))

    def test_move_down(self):
        self.mock_maze[1][0] = ' '
        self.player.move('s', self.mock_maze, self.mock_maze_obj)
        self.assertEqual(self.player.position, (0, 1))

    def test_move_left(self):
        self.mock_maze[0][1] = ' '
        self.player.position = (1, 0)
        self.player.move('a', self.mock_maze, self.mock_maze_obj)
        self.assertEqual(self.player.position, (0, 0))

    def test_move_right(self):
        self.mock_maze[0][1] = ' '
        self.player.move('d', self.mock_maze, self.mock_maze_obj)
        self.assertEqual(self.player.position, (1, 0))

    def test_collect_coin(self):
        self.mock_maze[0][1] = '🪙'
        self.player.move('d', self.mock_maze, self.mock_maze_obj)
        self.assertEqual(self.player.score, 10)
        self.assertEqual(self.mock_maze[0][1], ' ')
        self.mock_maze_obj.set_surface.assert_called_with(1, 0, None)

    def test_hit_trap(self):
        self.mock_maze[0][1] = '☠️'
        self.player.move('d', self.mock_maze, self.mock_maze_obj)
        self.assertEqual(self.player.score, -20)
        self.assertEqual(self.mock_maze[0][1], ' ')
        self.mock_maze_obj.set_surface.assert_called_with(1, 0, None)

    def test_increase_score(self):
        self.player.increase_score()
        self.assertEqual(self.player.score, 100)


if __name__ == '__main__':
    unittest.main()
