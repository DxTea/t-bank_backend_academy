import os
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock, call

from src.maze.maze import Maze
from src.view.renderer import ConsoleRenderer


class TestConsoleRenderer(unittest.TestCase):

    def test_init(self):
        renderer = ConsoleRenderer()
        self.assertIsNone(renderer.start)
        self.assertIsNone(renderer.start_symbol)
        self.assertIsNone(renderer.finish)
        self.assertIsNone(renderer.finish_symbol)

    def test_get_start_position(self):
        with patch('random.choice', return_value=(1, 0)):
            start, symbol = ConsoleRenderer.get_start_position()
            self.assertEqual(start, (1, 0))
            self.assertEqual(symbol, '⬇️')

    def test_get_finish_position(self):
        with patch('random.choice', return_value=(2, 3)):
            finish, symbol = ConsoleRenderer.get_finish_position(4, 4)
            self.assertEqual(finish, (2, 3))
            self.assertEqual(symbol, '⬇️')

    @patch('builtins.print')
    def test_display_exit_message(self, mock_print):
        ConsoleRenderer.display_exit_message()
        mock_print.assert_called_with("Спасибо за игру!")

    @patch('builtins.print')
    def test_display_error_message(self, mock_print):
        ConsoleRenderer.display_error_message()
        mock_print.assert_called_with(
            "Неверный выбор. Пожалуйста, попробуйте снова.")

    @patch('builtins.print')
    def test_render_maze_solved(self, mock_print):
        ConsoleRenderer.render_maze_solved()
        mock_print.assert_called_with("Лабиринт успешно решен!")

    @patch('builtins.print')
    def test_render_no_solution(self, mock_print):
        ConsoleRenderer.render_no_solution()
        mock_print.assert_called_with("Решение для лабиринта не найдено.")

    @patch('builtins.print')
    def test_render_options(self, mock_print):
        ConsoleRenderer.render_options()
        expected_calls = [
            call("\nОпции:"),
            call("1. Сгенерировать другой лабиринт с теми же параметрами"),
            call("2. Назад в меню"),
            call("3. Выйти")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)

    @patch('os.system')
    def test_display_welcome_screen(self, mock_system):
        renderer = ConsoleRenderer()
        with patch('builtins.print') as mock_print:
            renderer.display_welcome_screen()
            mock_system.assert_called_once_with(
                'cls' if os.name == 'nt' else 'clear')
            mock_print.assert_any_call("Добро пожаловать в игру Лабиринт!")
            mock_print.assert_any_call("Версия игры: 1.2.0")
            mock_print.assert_any_call("Разработчик: Семён Давыдов aka DxTea")
            mock_print.assert_any_call(
                "Инструкция: Поиграйте в прохождение лабиринта или "
                "выберите автоматическое решение одним из алгоритмов.")
            mock_print.assert_any_call("Лицензия: MIT")
            mock_print.assert_any_call("=========================")
            mock_print.assert_any_call("Нажмите ПРОБЕЛ, чтобы продолжить...")

    @patch('builtins.input', return_value='1')
    @patch('os.system')
    def test_preview_maze_size(self, mock_system, mock_input):
        result = ConsoleRenderer.preview_maze_size(5, 5)
        self.assertEqual(result, '1')
        mock_system.assert_called()

    @patch('builtins.print')
    def test_display_maze_info(self, mock_print):
        ConsoleRenderer.display_maze_info(
            first_algorithm='DFS',
            second_algorithm='BFS',
            width=10,
            height=10,
            surfaces_enabled=True,
            num_coins=5,
            num_traps=3,
            solution_algorithm='A*'
        )
        self.assertTrue(mock_print.called)

    @patch('builtins.input', return_value='5')
    @patch('os.system')
    def test_change_num_traps_menu(self, mock_system, mock_input):
        from src.view.renderer import ConsoleRenderer
        result = ConsoleRenderer.change_num_traps_menu()
        self.assertEqual(result, 5)
        mock_system.assert_called_once_with(
            'cls' if os.name == 'nt' else 'clear')

    @patch('builtins.input', return_value='10')
    @patch('os.system')
    def test_change_num_coins_menu(self, mock_system, mock_input):
        from src.view.renderer import ConsoleRenderer
        result = ConsoleRenderer.change_num_coins_menu()
        self.assertEqual(result, 10)
        mock_system.assert_called_once_with(
            'cls' if os.name == 'nt' else 'clear')

    @patch('os.system')
    def test_display_surfaces_menu(self, mock_system):
        from src.view.renderer import ConsoleRenderer
        menu = type('Menu', (object,),
                    {'surfaces_enabled': True, 'num_coins': 5,
                     'num_traps': 3})()
        with patch('builtins.print') as mock_print:
            ConsoleRenderer.display_surfaces_menu(menu)
            mock_print.assert_any_call("Настройки поверхностей")
            mock_print.assert_any_call("=================")
            mock_print.assert_any_call("Поверхности: Включены")
            mock_print.assert_any_call("Монеты: 5")
            mock_print.assert_any_call("Ловушки: 3")
        mock_system.assert_called_once_with(
            'cls' if os.name == 'nt' else 'clear')

    @patch('builtins.input', return_value='1')
    @patch('os.system')
    def test_display_menu(self, mock_system, mock_input):
        from src.view.renderer import ConsoleRenderer
        options = ["Option 1", "Option 2"]
        result = ConsoleRenderer.display_menu(options)
        self.assertEqual(result, 1)
        mock_system.assert_called_once_with(
            'cls' if os.name == 'nt' else 'clear')

    @patch('builtins.input', return_value='0')
    @patch('os.system')
    def test_display_algorithm_menu(self, mock_system, mock_input):
        from src.view.renderer import ConsoleRenderer
        algorithms = ["Algorithm 1", "Algorithm 2"]
        title = "Test"
        result = ConsoleRenderer.display_algorithm_menu(algorithms, title)
        self.assertEqual(result, 0)
        mock_system.assert_called_once_with(
            'cls' if os.name == 'nt' else 'clear')

    @patch('os.system')
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_common_settings(self, mock_stdout, mock_system):
        menu = MagicMock()
        menu.settings_manager.complicate_generation = True
        menu.settings_manager.selected_algorithms = ["Алгоритм1", "Алгоритм2"]
        menu.settings_manager.generation_algorithm = "Алгоритм1"
        menu.settings_manager.solution_algorithm = "АлгоритмРешения"
        menu.settings_manager.maze_size = "10x10"
        menu.settings_manager.surfaces_enabled = True

        ConsoleRenderer.display_common_settings(menu,
                                                show_solution_algorithm=True)

        expected_output = (
            "Текущие настройки:\n"
            "Алгоритм генерации: Алгоритм1 + Алгоритм2\n"
            "Алгоритм решения: АлгоритмРешения\n"
            "Размер лабиринта: 10x10\n"
            "Поверхности: Включены\n"
            "Усложненная генерация: Включена\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        mock_system.assert_called_with('cls' if os.name == 'nt' else 'clear')

    @patch('os.system')
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_complicate_generation_menu(self, mock_stdout,
                                                mock_system):
        menu = MagicMock()
        menu.settings_manager.complicate_generation = True

        ConsoleRenderer.display_complicate_generation_menu(menu)

        expected_output = (
            "Настройки усложненной генерации\n"
            "===============================\n"
            "Усложненная генерация: Включена\n"
            "1. Переключить усложненную генерацию\n"
            "2. Выбрать первый алгоритм\n"
            "3. Выбрать второй алгоритм\n"
            "4. Назад в предыдущее меню\n"
            "5. Выйти\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        mock_system.assert_called_with('cls' if os.name == 'nt' else 'clear')

    @patch.object(ConsoleRenderer, 'get_start_position',
                  return_value=((1, 1), 'S'))
    @patch.object(ConsoleRenderer, 'get_finish_position',
                  return_value=((3, 3), 'F'))
    def test_render_maze_initial_positions(self, mock_get_finish_position,
                                           mock_get_start_position):
        renderer = ConsoleRenderer()
        maze_mock = MagicMock(spec=Maze)
        maze_mock.get_maze.return_value = [['#', '#', '#'], ['#', ' ', '#'],
                                           ['#', '#', '#']]
        maze_mock.get_width.return_value = 3
        maze_mock.get_height.return_value = 3

        renderer.render_maze(maze_mock)

        self.assertEqual(renderer.start, (1, 1))
        self.assertEqual(renderer.start_symbol, 'S')
        self.assertEqual(renderer.finish, (3, 3))
        self.assertEqual(renderer.finish_symbol, 'F')

    def test_reset_positions(self):
        renderer = ConsoleRenderer()
        renderer.start = (1, 1)
        renderer.start_symbol = 'S'
        renderer.finish = (3, 3)
        renderer.finish_symbol = 'F'

        renderer.reset_positions()

        self.assertIsNone(renderer.start)
        self.assertIsNone(renderer.start_symbol)
        self.assertIsNone(renderer.finish)
        self.assertIsNone(renderer.finish_symbol)

    @patch('os.system')
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_build_maze_with_solution_menu(self, mock_stdout,
                                                   mock_system):
        menu = MagicMock()
        menu.settings_manager.generation_algorithm = "Случайный + Случайный"
        menu.settings_manager.solution_algorithm = "A*"
        menu.settings_manager.maze_size = "10x10"
        menu.settings_manager.surfaces_enabled = True
        menu.settings_manager.complicate_generation = True

        renderer = ConsoleRenderer()
        renderer.display_build_maze_with_solution_menu(menu)

        expected_output = (
            "Настройки построения лабиринта с решением\n"
            "=================================\n"
            "Текущие настройки:\n"
            "Алгоритм генерации: Случайный + Случайный\n"
            "Алгоритм решения: A*\n"
            "Размер лабиринта: 10x10\n"
            "Поверхности: Включены\n"
            "Усложненная генерация: Включена\n"
            "1. Построить лабиринт с решением\n"
            "2. Изменить алгоритм генерации\n"
            "3. Изменить алгоритм решения\n"
            "4. Изменить размер лабиринта\n"
            "5. Переключить поверхности\n"
            "6. Настройки усложненной генерации\n"
            "7. Назад в главное меню\n"
            "8. Выйти\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        mock_system.assert_has_calls([
            call('cls' if os.name == 'nt' else 'clear'),
            call('cls' if os.name == 'nt' else 'clear')
        ])

    @patch('os.system')
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_settings_menu(self, mock_stdout, mock_system):
        menu = MagicMock()
        menu.settings_manager.generation_algorithm = "Случайный + Случайный"
        menu.settings_manager.solution_algorithm = "A*"
        menu.settings_manager.maze_size = "10x10"
        menu.settings_manager.surfaces_enabled = True
        menu.settings_manager.complicate_generation = True

        renderer = ConsoleRenderer()
        renderer.display_game_settings_menu(menu)

        expected_output = (
            "Настройки игры\n"
            "=============\n"
            "Текущие настройки:\n"
            "Алгоритм генерации: Случайный + Случайный\n"
            "Размер лабиринта: 10x10\n"
            "Поверхности: Включены\n"
            "Усложненная генерация: Включена\n"
            "1. Начать игру\n"
            "2. Изменить алгоритм генерации\n"
            "3. Изменить размер лабиринта\n"
            "4. Переключить поверхности\n"
            "5. Настройки усложненной генерации\n"
            "6. Назад в главное меню\n"
            "7. Выйти\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        mock_system.assert_has_calls([
            call('cls' if os.name == 'nt' else 'clear'),
            call('cls' if os.name == 'nt' else 'clear')
        ])


if __name__ == '__main__':
    unittest.main()
