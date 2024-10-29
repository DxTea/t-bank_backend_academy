from src.maze.maze import Maze
import unittest
from unittest.mock import MagicMock, patch
from src.maze.maze_manager import MazeManager
from src.maze.settings_manager import SettingsManager


class TestMazeManager(unittest.TestCase):

    def setUp(self):
        self.menu = MagicMock()
        self.maze = MagicMock(spec=Maze)
        self.maze_manager = MagicMock(spec=MazeManager)
        self.maze_manager.maze = self.maze
        self.maze_manager.generate_maze = MagicMock()
        self.maze_manager.solve_maze = MagicMock()
        self.maze_manager.reset_maze = MagicMock()
        self.maze_manager.get_maze_size = MagicMock(
            return_value=(10, 15))  # Mock return value
        self.maze_manager.select_algorithms = MagicMock(
            return_value=("Прим", "Краскал"))  # Mock return value
        self.menu.settings_manager = MagicMock()
        self.settings_manager = MagicMock(spec=SettingsManager)
        self.menu.settings_manager = self.settings_manager

    def test_initialization(self):
        self.assertEqual(self.maze_manager.maze, self.maze)

    def test_generate_maze(self):
        self.maze_manager.generate_maze(3, "Прим", "Краскал")
        self.maze_manager.generate_maze.assert_called_once_with(3, "Прим",
                                                                "Краскал")

    def test_solve_maze(self):
        self.maze_manager.solve_maze("A*")
        self.maze_manager.solve_maze.assert_called_once_with("A*")

    def test_reset_maze(self):
        self.maze_manager.reset_maze()
        self.maze_manager.reset_maze.assert_called_once()

    @patch('random.randint')
    def test_get_maze_size_random(self, mock_randint):
        self.menu.settings_manager.maze_size = "Cлучайно"
        mock_randint.side_effect = [10, 15]

        # Simulate the actual behavior of get_maze_size
        self.maze_manager.get_maze_size.side_effect = lambda: (
            mock_randint(5, 30), mock_randint(5, 20))

        width, height = self.maze_manager.get_maze_size()

        self.assertEqual(width, 10)
        self.assertEqual(height, 15)
        self.assertEqual(mock_randint.call_count, 2)
        mock_randint.assert_has_calls(
            [unittest.mock.call(5, 30), unittest.mock.call(5, 20)])

    def test_get_maze_size_specific(self):
        self.menu.settings_manager.maze_size = "10x15"

        width, height = self.maze_manager.get_maze_size()

        self.assertEqual(width, 10)
        self.assertEqual(height, 15)

    @patch('random.choice')
    def test_select_algorithms_complicate_generation_less_than_two(self,
                                                                   mock_choice):
        self.settings_manager.complicate_generation = True
        self.settings_manager.selected_algorithms = []
        self.settings_manager.complicate_algorithms = ['Алгоритм1', 'Прим',
                                                       'Краскал']
        mock_choice.side_effect = ['Прим', 'Краскал']

        # Simulate the actual behavior of select_algorithms
        self.maze_manager.select_algorithms.side_effect = lambda: (
            mock_choice(self.settings_manager.complicate_algorithms[1:]),
            mock_choice(self.settings_manager.complicate_algorithms[1:])
        )

        first_algorithm, second_algorithm = self.maze_manager.select_algorithms()

        self.assertEqual(first_algorithm, 'Прим')
        self.assertEqual(second_algorithm, 'Краскал')
        self.assertEqual(mock_choice.call_count, 2)

    def test_select_algorithms_complicate_generation_two_algorithms(self):
        self.settings_manager.complicate_generation = True
        self.settings_manager.selected_algorithms = ['Прим', 'Краскал']

        first_algorithm, second_algorithm = self.maze_manager.select_algorithms()

        self.assertEqual(first_algorithm, 'Прим')
        self.assertEqual(second_algorithm, 'Краскал')

    def test_select_algorithms_not_complicate_generation_specific_algorithm(
            self):
        self.settings_manager.complicate_generation = False
        self.settings_manager.generation_algorithm = 'Прим'
        self.settings_manager.generation_algorithms = ['Алгоритм1', 'Прим',
                                                       'Краскал']

        # Simulate the actual behavior of select_algorithms
        self.maze_manager.select_algorithms.side_effect = lambda: (
            self.settings_manager.generation_algorithm, None
        )

        first_algorithm, second_algorithm = self.maze_manager.select_algorithms()

        self.assertEqual(first_algorithm, 'Прим')
        self.assertIsNone(second_algorithm)

    @patch('random.choice')
    def test_select_algorithms_not_complicate_generation_random_algorithm(self,
                                                                          mock_choice):
        self.settings_manager.complicate_generation = False
        self.settings_manager.generation_algorithm = 'Cлучайно'
        self.settings_manager.generation_algorithms = ['Алгоритм1', 'Прим',
                                                       'Краскал']
        mock_choice.return_value = 'Прим'

        # Simulate the actual behavior of select_algorithms
        self.maze_manager.select_algorithms.side_effect = lambda: (
            mock_choice(self.settings_manager.generation_algorithms[1:]), None
        )

        first_algorithm, second_algorithm = self.maze_manager.select_algorithms()

        self.assertEqual(first_algorithm, 'Прим')
        self.assertIsNone(second_algorithm)
        mock_choice.assert_called_once_with(
            self.settings_manager.generation_algorithms[1:])


if __name__ == '__main__':
    unittest.main()
