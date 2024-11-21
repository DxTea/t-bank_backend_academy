import unittest
from unittest.mock import MagicMock, patch
from src.maze.settings_manager import SettingsManager


class TestSettingsManager(unittest.TestCase):

    def setUp(self):
        self.menu = MagicMock()
        self.settings_manager = SettingsManager(self.menu)

    def test_initialization(self):
        self.assertEqual(self.settings_manager.generation_algorithm,
                         "Cлучайно")
        self.assertEqual(self.settings_manager.solution_algorithm, "Cлучайно")
        self.assertEqual(self.settings_manager.maze_size, "Cлучайно")
        self.assertFalse(self.settings_manager.surfaces_enabled)
        self.assertEqual(self.settings_manager.num_coins, 0)
        self.assertEqual(self.settings_manager.num_traps, 0)
        self.assertFalse(self.settings_manager.complicate_generation)
        self.assertEqual(self.settings_manager.complicate_algorithms, [
            "Cлучайно", "Краскал", "Прим",
            "Рекурсивное обратное отслеживание",
            "Двоичное дерево"])
        self.assertEqual(self.settings_manager.selected_algorithms, [])
        self.assertEqual(self.settings_manager.generation_algorithms, [
            "Cлучайно", "Краскал", "Прим",
            "Рекурсивное обратное отслеживание",
            "Двоичное дерево"])
        self.assertEqual(self.settings_manager.solution_algorithms, [
            "Cлучайно", "A*", "BFS", "DFS", "Форд-Беллман"])

    def test_select_first_algorithm(self):
        self.menu.algorithm_menu.return_value = 2
        self.settings_manager.select_first_algorithm()
        self.assertEqual(self.settings_manager.selected_algorithms, ["Прим"])

    def test_select_second_algorithm(self):
        self.menu.algorithm_menu.side_effect = [2, 3]
        self.settings_manager.select_first_algorithm()
        self.settings_manager.select_second_algorithm()
        self.assertEqual(self.settings_manager.selected_algorithms,
                         ["Прим", "Рекурсивное обратное отслеживание"])

    def test_change_solution_algorithm(self):
        self.menu.algorithm_menu.return_value = 1
        self.settings_manager.change_solution_algorithm()
        self.assertEqual(self.settings_manager.solution_algorithm, "A*")
        self.menu.algorithm_menu.assert_called_once_with(
            self.settings_manager.solution_algorithms, "Алгоритм решения")

    @patch('builtins.input',
           return_value='')
    def test_change_generation_algorithm_complicate_generation(self,
                                                               mock_input):
        self.settings_manager.complicate_generation = True
        with patch('builtins.print') as mock_print:
            self.settings_manager.change_generation_algorithm()
            mock_print.assert_any_call(
                "Чтобы выбрать алгоритм, сначала необходимо отключить "
                "настройки усложненной генерации.")
            mock_input.assert_called_once()

    def test_change_generation_algorithm(self):
        self.settings_manager.complicate_generation = False
        self.menu.algorithm_menu.return_value = 1
        with patch('builtins.print') as mock_print:
            self.settings_manager.change_generation_algorithm()
            self.assertEqual(self.settings_manager.generation_algorithm,
                             "Краскал")
            self.assertEqual(self.menu.generation_algorithm, "Краскал")
            self.menu.algorithm_menu.assert_called_once_with(
                self.settings_manager.generation_algorithms,
                "Алгоритм генерации")
            mock_print.assert_any_call(
                "Алгоритм генерации изменен на: Краскал")

    def test_change_maze_size_option_1(self):
        self.menu.input_handler.get_maze_size.return_value = (10, 15)
        self.menu.renderer.preview_maze_size.return_value = '1'

        self.settings_manager.change_maze_size()

        self.assertEqual(self.settings_manager.maze_size, "10x15")
        self.assertEqual(self.menu.maze_size, "10x15")
        self.menu.input_handler.get_maze_size.assert_called_once()
        self.menu.renderer.preview_maze_size.assert_called_once_with(10, 15)

    def test_change_maze_size_option_2(self):
        self.menu.input_handler.get_maze_size.side_effect = [(10, 15),
                                                             (20, 25)]
        self.menu.renderer.preview_maze_size.side_effect = ['2', '1']

        self.settings_manager.change_maze_size()

        self.assertEqual(self.settings_manager.maze_size, "20x25")
        self.assertEqual(self.menu.maze_size, "20x25")
        self.assertEqual(self.menu.input_handler.get_maze_size.call_count, 2)
        self.assertEqual(self.menu.renderer.preview_maze_size.call_count, 2)

    def test_change_maze_size_option_3(self):
        self.menu.input_handler.get_maze_size.return_value = (10, 15)
        self.menu.renderer.preview_maze_size.return_value = '3'

        self.settings_manager.change_maze_size()

        self.assertNotEqual(self.settings_manager.maze_size, "10x15")
        self.menu.input_handler.get_maze_size.assert_called_once()
        self.menu.renderer.preview_maze_size.assert_called_once_with(10, 15)

    def test_toggle_surfaces(self):
        initial_state = self.settings_manager.surfaces_enabled
        self.settings_manager.toggle_surfaces()
        self.assertEqual(self.settings_manager.surfaces_enabled,
                         not initial_state)
        self.assertEqual(self.menu.surfaces_enabled, not initial_state)

    @patch('builtins.print')
    def test_toggle_surfaces_print(self, mock_print):
        self.settings_manager.toggle_surfaces()
        mock_print.assert_called_once_with(
            f"Поверхности включены: {self.settings_manager.surfaces_enabled}")


if __name__ == '__main__':
    unittest.main()
