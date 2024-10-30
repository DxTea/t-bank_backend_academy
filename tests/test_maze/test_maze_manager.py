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
            return_value=(10, 15))
        self.maze_manager.select_algorithms = MagicMock(
            return_value=("Прим", "Краскал"))
        self.menu.settings_manager = MagicMock()
        self.settings_manager = MagicMock(spec=SettingsManager)
        self.menu.settings_manager = self.settings_manager
        self.menu.renderer = MagicMock()
        self.menu.input_handler = MagicMock()

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
    def test_select_algorithms_complicate_generation_less_than_two(
            self,
            mock_choice):
        self.settings_manager.complicate_generation = True
        self.settings_manager.selected_algorithms = []
        self.settings_manager.complicate_algorithms = ['Алгоритм1', 'Прим',
                                                       'Краскал']
        mock_choice.side_effect = ['Прим', 'Краскал']

        self.maze_manager.select_algorithms.side_effect = lambda: (
            mock_choice(self.settings_manager.complicate_algorithms[1:]),
            mock_choice(self.settings_manager.complicate_algorithms[1:])
        )

        first_algorithm, second_algorithm = (self.
                                             maze_manager.select_algorithms())

        self.assertEqual(first_algorithm, 'Прим')
        self.assertEqual(second_algorithm, 'Краскал')
        self.assertEqual(mock_choice.call_count, 2)

    def test_select_algorithms_complicate_generation_two_algorithms(self):
        self.settings_manager.complicate_generation = True
        self.settings_manager.selected_algorithms = ['Прим', 'Краскал']

        first_algorithm, second_algorithm = (self.
                                             maze_manager.select_algorithms())

        self.assertEqual(first_algorithm, 'Прим')
        self.assertEqual(second_algorithm, 'Краскал')

    def test_select_algorithms_not_complicate_generation_specific_algorithm(
            self):
        self.settings_manager.complicate_generation = False
        self.settings_manager.generation_algorithm = 'Прим'
        self.settings_manager.generation_algorithms = ['Алгоритм1', 'Прим',
                                                       'Краскал']

        self.maze_manager.select_algorithms.side_effect = lambda: (
            self.settings_manager.generation_algorithm, None
        )

        first_algorithm, second_algorithm = (self.
                                             maze_manager.select_algorithms())

        self.assertEqual(first_algorithm, 'Прим')
        self.assertIsNone(second_algorithm)

    @patch('random.choice')
    def test_select_algorithms_not_complicate_generation_random_algorithm(
            self,
            mock_choice):
        self.settings_manager.complicate_generation = False
        self.settings_manager.generation_algorithm = 'Cлучайно'
        self.settings_manager.generation_algorithms = ['Алгоритм1', 'Прим',
                                                       'Краскал']
        mock_choice.return_value = 'Прим'

        self.maze_manager.select_algorithms.side_effect = lambda: (
            mock_choice(self.settings_manager.generation_algorithms[1:]), None
        )

        first_algorithm, second_algorithm = (self.
                                             maze_manager.select_algorithms())

        self.assertEqual(first_algorithm, 'Прим')
        self.assertIsNone(second_algorithm)
        mock_choice.assert_called_once_with(
            self.settings_manager.generation_algorithms[1:])

    @patch('src.maze.maze_manager.Game')
    @patch('src.maze.maze_manager.MazeManager.get_maze_size',
           return_value=(10, 15))
    @patch('src.maze.maze_manager.MazeManager.select_algorithms',
           return_value=("Прим", "Краскал"))
    @patch('src.maze.maze_manager.MazeManager.generate_maze')
    @patch('src.maze.maze_manager.MazeManager.place_surfaces')
    def test_start_game(self, mock_place_surfaces, mock_generate_maze,
                        mock_select_algorithms, mock_get_maze_size, mock_game):
        mock_maze = MagicMock()
        mock_generate_maze.return_value = mock_maze
        mock_game_instance = MagicMock()
        mock_game.return_value = mock_game_instance

        self.settings_manager.surfaces_enabled = True
        self.settings_manager.num_coins = 10
        self.settings_manager.num_traps = 5

        maze_manager = MazeManager(
            self.menu)

        maze_manager.start_game()

        mock_get_maze_size.assert_called_once()
        mock_select_algorithms.assert_called_once()
        mock_generate_maze.assert_called_once_with(10, 15, "Прим", "Краскал")
        mock_place_surfaces.assert_called_once_with(mock_maze)
        mock_game.assert_called_once_with(mock_maze)
        mock_game_instance.play.assert_called_once()
        self.menu.renderer.display_maze_info.assert_called_once_with("Прим",
                                                                     "Краскал",
                                                                     10, 15,
                                                                     True, 10,
                                                                     5)

    @patch('random.choice')
    @patch('src.maze.maze_manager.Solver')
    def test_build_maze_with_solution_solved(self, mock_solver,
                                             mock_random_choice):
        mock_solver_instance = MagicMock()
        mock_solver_instance.solve.return_value = True
        mock_solver_instance.maze = self.maze
        mock_solver.return_value = mock_solver_instance
        mock_random_choice.return_value = "A*"

        self.menu.settings_manager.solution_algorithm = "Cлучайно"
        self.menu.settings_manager.solution_algorithms = ["Алгоритм1", "A*"]
        self.menu.settings_manager.surfaces_enabled = True
        self.menu.settings_manager.num_coins = 10
        self.menu.settings_manager.num_traps = 5

        maze_manager = MazeManager(
            self.menu)

        with patch.object(maze_manager, 'get_maze_size',
                          return_value=(10, 15)):
            with patch.object(maze_manager, 'select_algorithms',
                              return_value=("Прим", "Краскал")):
                with patch.object(maze_manager, 'generate_maze',
                                  return_value=self.maze):
                    with patch.object(maze_manager, 'place_surfaces'):
                        self.menu.input_handler.get_choice.side_effect = ['2']

                        maze_manager.build_maze_with_solution()

                        mock_solver.assert_called_once_with("A*", self.maze)
                        mock_solver_instance.solve.assert_called_once()
                        self.menu.renderer.render_maze.assert_called_once_with(
                            self.maze)
                        self.menu.renderer.display_maze_info.assert_called_once_with(
                            "Прим", "Краскал", 10, 15, True, 10, 5, "A*")
                        self.menu.renderer.render_maze_solved.assert_called_once()
                        self.menu.renderer.render_options.assert_called_once()
                        self.menu.renderer.reset_positions.assert_called_once()

    @patch('random.choice')
    @patch('src.maze.maze_manager.Solver')
    def test_build_maze_with_solution_not_solved(self, mock_solver,
                                                 mock_random_choice):
        mock_solver_instance = MagicMock()
        mock_solver_instance.solve.return_value = False
        mock_solver.return_value = mock_solver_instance
        mock_random_choice.return_value = "A*"

        self.menu.settings_manager.solution_algorithm = "Cлучайно"
        self.menu.settings_manager.solution_algorithms = ["Алгоритм1", "A*"]
        self.menu.settings_manager.surfaces_enabled = True
        self.menu.settings_manager.num_coins = 10
        self.menu.settings_manager.num_traps = 5

        maze_manager = MazeManager(
            self.menu)

        with patch.object(maze_manager, 'get_maze_size',
                          return_value=(10, 15)):
            with patch.object(maze_manager, 'select_algorithms',
                              return_value=("Прим", "Краскал")):
                with patch.object(maze_manager, 'generate_maze',
                                  return_value=self.maze):
                    with patch.object(maze_manager, 'place_surfaces'):
                        self.menu.input_handler.get_choice.side_effect = ['2']

                        maze_manager.build_maze_with_solution()

                        mock_solver.assert_called_once_with("A*", self.maze)
                        mock_solver_instance.solve.assert_called_once()
                        self.menu.renderer.render_maze.assert_called_once_with(
                            self.maze)
                        self.menu.renderer.display_maze_info.assert_called_once_with(
                            "Прим", "Краскал", 10, 15, True, 10, 5)
                        self.menu.renderer.render_no_solution.assert_called_once()
                        self.menu.renderer.render_options.assert_called_once()
                        self.menu.renderer.reset_positions.assert_called_once()


if __name__ == '__main__':
    unittest.main()
