import unittest
from unittest.mock import MagicMock, patch
from src.view.renderer import ConsoleRenderer
from src.game.game import Game
from src.maze.maze import Maze


class TestGame(unittest.TestCase):

    def setUp(self):
        self.mock_maze = MagicMock(spec=Maze)
        self.mock_maze.get_maze.return_value = [[' ' for _ in range(5)] for _
                                                in range(5)]
        self.mock_maze.start = (0, 0)
        self.mock_maze.finish = (4, 4)
        self.game = Game(self.mock_maze)

    def test_initialization(self):
        self.assertEqual(self.game.maze,
                         [[' ' for _ in range(5)] for _ in range(5)])
        self.assertEqual(self.game.player.position, (0, 0))
        self.assertEqual(self.game.exit, (4, 4))
        self.assertIsInstance(self.game.renderer, ConsoleRenderer)
        self.assertFalse(self.game.game_started)

    @patch('builtins.input', return_value='0')
    @patch('src.view.renderer.ConsoleRenderer.render_game')
    def test_play_exit(self, mock_render_game, mock_input):
        with self.assertRaises(SystemExit):
            self.game.play()
        self.assertTrue(self.game.game_started)
        mock_render_game.assert_called()

    @patch('builtins.input', side_effect=['w', 's', 'a', 'd', '0'])
    @patch('src.view.renderer.ConsoleRenderer.render_game')
    def test_play_moves(self, mock_render_game, mock_input):
        with self.assertRaises(SystemExit):
            self.game.play()
        self.assertTrue(self.game.game_started)
        self.assertEqual(self.game.player.position,
                         (1, 1))
        mock_render_game.assert_called()

    @patch('src.game.game.Game.display_game_settings_menu',
           return_value='main_menu')
    @patch('builtins.input', return_value='1')
    def test_play_settings_menu(self, mock_input,
                                mock_display_game_settings_menu):
        result = self.game.play()
        self.assertEqual(result, None)
        mock_display_game_settings_menu.assert_called_once()

    @patch('src.handlers.menu_handler.Menu.game_settings_menu',
           return_value=None)
    def test_display_game_settings_menu(self, mock_game_settings_menu):
        result = self.game.display_game_settings_menu()
        self.assertIsNone(result)
        mock_game_settings_menu.assert_called_once()


if __name__ == '__main__':
    unittest.main()
