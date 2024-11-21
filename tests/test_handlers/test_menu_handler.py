import unittest
from unittest.mock import MagicMock, patch
from src.handlers.menu_handler import Menu
from src.view.renderer import ConsoleRenderer
from src.handlers.input_handler import InputHandler
from src.maze.settings_manager import SettingsManager
from src.maze.maze_manager import MazeManager


class TestMenu(unittest.TestCase):

    def setUp(self):
        self.menu = Menu()
        self.menu.renderer = MagicMock(spec=ConsoleRenderer)
        self.menu.input_handler = MagicMock(spec=InputHandler)
        self.menu.settings_manager = MagicMock(spec=SettingsManager)
        self.menu.maze_manager = MagicMock(spec=MazeManager)
        self.menu._surfaces_menu = MagicMock()
        self.menu._complicate_generation_menu = MagicMock()
        self.menu.exit_game = MagicMock()
        self.menu.settings_manager.selected_algorithms = ['Прим', 'Краскал']
        self.menu.main_menu = MagicMock()

    @patch('builtins.input', return_value='1')
    def test_build_maze_with_solution_menu_option_1(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['1', '7'])
        self.menu._build_maze_with_solution_menu()
        self.menu.maze_manager.build_maze_with_solution.assert_called_once()

    @patch('builtins.input', return_value='2')
    def test_build_maze_with_solution_menu_option_2(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['2', '7'])
        self.menu.settings_manager.complicate_generation = False
        self.menu._build_maze_with_solution_menu()
        (self.menu.settings_manager.change_generation_algorithm
         .assert_called_once())

    @patch('builtins.input', return_value='3')
    def test_build_maze_with_solution_menu_option_3(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['3', '7'])
        self.menu._build_maze_with_solution_menu()
        (self.menu.settings_manager.change_solution_algorithm
         .assert_called_once())

    @patch('builtins.input', return_value='5')
    def test_build_maze_with_solution_menu_option_5(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['5', '7'])
        self.menu._build_maze_with_solution_menu()
        self.menu._surfaces_menu.assert_called_once()

    @patch('builtins.input', return_value='6')
    def test_build_maze_with_solution_menu_option_6(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['6', '7'])
        self.menu._build_maze_with_solution_menu()
        self.menu._complicate_generation_menu.assert_called_once()

    @patch('builtins.input', return_value='7')
    def test_build_maze_with_solution_menu_option_7(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            return_value='7')
        self.menu._build_maze_with_solution_menu()

    @patch('builtins.input', return_value='1')
    def test_complicate_generation_menu_option_1(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['1', '4'])

        self.menu.settings_manager.complicate_generation = False

        self.menu._complicate_generation_menu()
        self.menu.settings_manager.complicate_generation = True
        self.assertTrue(self.menu.settings_manager.complicate_generation)

    @patch('builtins.input', return_value='4')
    def test_complicate_generation_menu_option_4(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            return_value='4')
        self.menu._complicate_generation_menu()

    @patch('builtins.input', return_value='4')
    def test_surfaces_menu_option_4(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            return_value='4')
        self.menu._surfaces_menu()

    @patch('builtins.input', side_effect=['2', '4'])
    def test_complicate_generation_menu_option_2(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['2', '4'])

        self.menu._complicate_generation_menu = (
            Menu._complicate_generation_menu.__get__(self.menu))

        self.menu._complicate_generation_menu()
        self.menu.settings_manager.select_first_algorithm.assert_called_once()

        self.assertIn('Прим', self.menu.settings_manager.selected_algorithms)

    @patch('builtins.input', return_value='3')
    def test_complicate_generation_menu_option_3(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['3', '4'])
        self.menu._complicate_generation_menu = (
            Menu._complicate_generation_menu.__get__(self.menu))

        self.menu._complicate_generation_menu()
        self.menu.settings_manager.select_second_algorithm.assert_called_once()

        self.assertIn('Краскал',
                      self.menu.settings_manager.selected_algorithms)

    @patch('builtins.input', side_effect=['5', '4'])
    def test_complicate_generation_menu_option_5(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['5', '4'])

        self.menu._complicate_generation_menu = (
            Menu._complicate_generation_menu.__get__(self.menu))

        self.menu._complicate_generation_menu()

        self.menu.exit_game.assert_called_once()

    @patch('builtins.input', side_effect=['1', '4'])
    def test_surfaces_menu_option_1(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['1', '4'])

        self.menu._surfaces_menu = Menu._surfaces_menu.__get__(self.menu)
        self.menu._surfaces_menu()
        self.menu.settings_manager.toggle_surfaces.assert_called_once()

    @patch('builtins.input', side_effect=['2', '4'])
    def test_surfaces_menu_option_2(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['2', '4'])

        self.menu._surfaces_menu = Menu._surfaces_menu.__get__(self.menu)
        self.menu._surfaces_menu()
        self.menu.settings_manager.change_num_coins.assert_called_once()

    @patch('builtins.input', side_effect=['3', '4'])
    def test_surfaces_menu_option_3(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['3', '4'])

        self.menu._surfaces_menu = Menu._surfaces_menu.__get__(self.menu)
        self.menu._surfaces_menu()
        self.menu.settings_manager.change_num_traps.assert_called_once()

    @patch('builtins.input', side_effect=['5', '4'])
    def test_surfaces_menu_option_5(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['5', '4'])

        self.menu._surfaces_menu = Menu._surfaces_menu.__get__(self.menu)
        self.menu._surfaces_menu()
        self.menu.exit_game.assert_called_once()

    @patch('builtins.input', side_effect=['invalid', '4'])
    def test_surfaces_menu_invalid_option(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['invalid',
                         '4'])

        self.menu._surfaces_menu = Menu._surfaces_menu.__get__(self.menu)
        self.menu._surfaces_menu()
        self.menu.renderer.display_error_message.assert_called_once()

    @patch('builtins.input', return_value='1')
    def test_game_settings_menu_option_1(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['1', '6'])
        self.menu.game_settings_menu()
        self.menu.maze_manager.start_game.assert_called_once()

    @patch('builtins.input', return_value='2')
    def test_game_settings_menu_option_2(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['2', '6'])
        self.menu.settings_manager.complicate_generation = False
        self.menu.game_settings_menu()
        (self.menu.settings_manager.
         change_generation_algorithm.assert_called_once())

    @patch('builtins.input', return_value='3')
    def test_game_settings_menu_option_3(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['3', '6'])
        self.menu.game_settings_menu()
        self.menu.settings_manager.change_maze_size.assert_called_once()

    @patch('builtins.input', return_value='4')
    def test_game_settings_menu_option_4(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['4', '6'])
        self.menu.game_settings_menu()
        self.menu._surfaces_menu.assert_called_once()

    @patch('builtins.input', return_value='5')
    def test_game_settings_menu_option_5(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['5', '6'])
        self.menu.game_settings_menu()
        self.menu._complicate_generation_menu.assert_called_once()

    @patch('builtins.input', return_value='6')
    def test_game_settings_menu_option_6(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            return_value='6')
        self.menu.game_settings_menu()
        self.menu.main_menu.assert_called_once()

    @patch('builtins.input', return_value='7')
    def test_game_settings_menu_option_7(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['7', '6'])
        self.menu.game_settings_menu()
        self.menu.exit_game.assert_called_once()

    @patch('builtins.input', return_value='invalid')
    def test_game_settings_menu_invalid_option(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['invalid',
                         '6'])
        self.menu.game_settings_menu()
        self.menu.renderer.display_error_message.assert_called_once()

    @patch('builtins.input', return_value='1')
    def test_main_menu_option_1(self, mock_input):
        self.menu.renderer.display_menu = MagicMock(return_value=1)
        self.menu.main_menu = Menu.main_menu.__get__(self.menu)
        choice = self.menu.main_menu()
        self.assertEqual(choice, 1)

    @patch('builtins.input', return_value='2')
    def test_main_menu_option_2(self, mock_input):
        self.menu.renderer.display_menu = MagicMock(return_value=2)
        self.menu.main_menu = Menu.main_menu.__get__(self.menu)
        choice = self.menu.main_menu()
        self.assertEqual(choice, 2)

    @patch('builtins.input', return_value='3')
    def test_main_menu_option_3(self, mock_input):
        self.menu.renderer.display_menu = MagicMock(return_value=3)
        self.menu.main_menu = Menu.main_menu.__get__(self.menu)
        choice = self.menu.main_menu()
        self.assertEqual(choice, 3)

    @patch.object(Menu, 'game_settings_menu')
    def test_handle_choice_option_1(self, mock_game_settings_menu):
        self.menu.handle_choice(1)
        mock_game_settings_menu.assert_called_once()

    @patch.object(Menu, '_build_maze_with_solution_menu')
    def test_handle_choice_option_2(self, mock_build_maze_with_solution_menu):
        self.menu.handle_choice(2)
        mock_build_maze_with_solution_menu.assert_called_once()

    @patch.object(Menu, 'exit_game')
    def test_handle_choice_option_3(self, mock_exit_game):
        self.menu.handle_choice(3)
        self.menu.exit_game.assert_called_once()

    def test_handle_choice_invalid_option(self):
        self.menu.renderer.display_error_message = MagicMock()
        self.menu.handle_choice(4)
        self.menu.renderer.display_error_message.assert_called_once()


if __name__ == '__main__':
    unittest.main()
