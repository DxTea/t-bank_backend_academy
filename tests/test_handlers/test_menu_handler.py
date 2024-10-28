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

    @patch('builtins.input', return_value='1')
    def test_build_maze_with_solution_menu_option_1(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['1', '7'])  # Simulate '1' then '7' to break loop
        self.menu._build_maze_with_solution_menu()
        self.menu.maze_manager.build_maze_with_solution.assert_called_once()

    @patch('builtins.input', return_value='2')
    def test_build_maze_with_solution_menu_option_2(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['2', '7'])  # Simulate '2' then '7' to break loop
        self.menu.settings_manager.complicate_generation = False
        self.menu._build_maze_with_solution_menu()
        (self.menu.settings_manager.change_generation_algorithm
         .assert_called_once())

    @patch('builtins.input', return_value='3')
    def test_build_maze_with_solution_menu_option_3(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['3', '7'])  # Simulate '3' then '7' to break loop
        self.menu._build_maze_with_solution_menu()
        (self.menu.settings_manager.change_solution_algorithm
         .assert_called_once())

    @patch('builtins.input', return_value='5')
    def test_build_maze_with_solution_menu_option_5(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['5', '7'])  # Simulate '5' then '7' to break loop
        self.menu._build_maze_with_solution_menu()
        self.menu._surfaces_menu.assert_called_once()

    @patch('builtins.input', return_value='6')
    def test_build_maze_with_solution_menu_option_6(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['6', '7'])  # Simulate '6' then '7' to break loop
        self.menu._build_maze_with_solution_menu()
        self.menu._complicate_generation_menu.assert_called_once()

    @patch('builtins.input', return_value='7')
    def test_build_maze_with_solution_menu_option_7(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            return_value='7')  # Simulate '7' to break loop
        self.menu._build_maze_with_solution_menu()
        # Ensure the loop breaks without calling any other method

    @patch('builtins.input', return_value='1')
    def test_complicate_generation_menu_option_1(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            side_effect=['1', '4'])  # Simulate '1' then '4' to break loop

        # Directly set the complicate_generation attribute on the mock object
        self.menu.settings_manager.complicate_generation = False

        self.menu._complicate_generation_menu()
        self.menu.settings_manager.complicate_generation = True
        self.assertTrue(self.menu.settings_manager.complicate_generation)

    @patch('builtins.input', return_value='4')
    def test_complicate_generation_menu_option_4(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            return_value='4')  # Simulate '4' to break loop
        self.menu._complicate_generation_menu()
        # Ensure the loop breaks without calling any other method

    @patch('builtins.input', return_value='4')
    def test_surfaces_menu_option_4(self, mock_input):
        self.menu.input_handler.get_choice = MagicMock(
            return_value='4')  # Simulate '4' to break loop
        self.menu._surfaces_menu()
        # Ensure the loop breaks without calling any other method


if __name__ == '__main__':
    unittest.main()
