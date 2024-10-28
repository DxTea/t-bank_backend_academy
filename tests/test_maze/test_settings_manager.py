import unittest
from unittest.mock import MagicMock
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
        self.menu.algorithm_menu.return_value = 2  # Mock user selecting "Прим"
        self.settings_manager.select_first_algorithm()
        self.assertEqual(self.settings_manager.selected_algorithms, ["Прим"])

    def test_select_second_algorithm(self):
        self.menu.algorithm_menu.side_effect = [2, 3]  # Mock user selections
        self.settings_manager.select_first_algorithm()
        self.settings_manager.select_second_algorithm()
        self.assertEqual(self.settings_manager.selected_algorithms,
                         ["Прим", "Рекурсивное обратное отслеживание"])


if __name__ == '__main__':
    unittest.main()
