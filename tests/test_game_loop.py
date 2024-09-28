import unittest
from unittest.mock import patch, MagicMock

from src.custom_errors import InvalidMenuChoiceError
from src.error_handler import ErrorHandler
from src.game_loop import GameLoop
from src.word_dictionary import WordDictionary


class TestGameLoop(unittest.TestCase):
    def setUp(self):
        """
        Метод для установки начальных условий перед каждым тестом.
        """
        self.word_dictionary = WordDictionary()
        self.game_loop = GameLoop(self.word_dictionary)
        self.error_handler = ErrorHandler()

    @patch('src.game_loop.InputHandler')
    def test_handle_hint_with_invalid_hint(self, mock_input_handler):
        """
        Тест проверяет обработку подсказки с недопустимым значением.
        """
        mock_input_handler.get_user_input.return_value = "3"
        mock_input_handler.validate_hint_usage.side_effect = \
            InvalidMenuChoiceError("Invalid hint choice")
        mock_game = MagicMock()
        with self.assertRaises(InvalidMenuChoiceError):
            self.game_loop.handle_hint("3",
                                       ["1. Подсказка 1", "2. Подсказка 2"],
                                       mock_game)

    @patch('src.game_loop.InputHandler')
    def test_handle_hint(self, mock_input_handler):
        """
        Тест проверяет обработку подсказки.
        """
        mock_input_handler.get_user_input.return_value = "1"
        mock_input_handler.validate_hint_usage.side_effect = None
        mock_game = MagicMock()
        mock_game.current_word.hints.__getitem__.return_value = "Test hint"
        self.game_loop.handle_hint("1", ["1. Подсказка 1", "2. Подсказка 2"],
                                   mock_game)
        mock_input_handler.validate_hint_usage.assert_called_once_with(0, [
            "Подсказка 1: Test hint", "2. Подсказка 2"])

    @patch('src.game_loop.InputHandler')
    def test_handle_main_menu_choice(self, mock_input_handler):
        """
        Тест проверяет обработку выбора в главном меню.
        """
        mock_input_handler.get_user_input.side_effect = ["1", "4"]
        mock_input_handler.validate_menu_choice.return_value = "1"
        with self.assertRaises(SystemExit):
            self.game_loop.run()
        mock_input_handler.validate_menu_choice.assert_called_with("1",
                                                                   ["1", "2",
                                                                    "3", "4"])

    @patch('src.game_loop.InputHandler.get_user_input', side_effect=['3', '2'])
    @patch('src.game_loop.Renderer.render_post_game_menu')
    def test_post_game_handle_error(self, mock_render_menu, mock_get_input):
        game_loop = GameLoop(MagicMock())
        game_loop.error_handler = MagicMock()
        with self.assertRaises(SystemExit):
            game_loop.post_game()
        call_args = game_loop.error_handler.handle_error.call_args
        assert isinstance(call_args[0][0], InvalidMenuChoiceError)
        assert str(call_args[0][
                       0]) == ("Недопустимый ввод: '3'. Пожалуйста, "
                               "введите номер пункта меню.")

    def test_reset_settings(self):
        """
        Тест проверяет сброс настроек.
        """
        self.game_loop.reset_settings()
        self.assertEqual(self.game_loop.difficulty, "Случайно")
        self.assertEqual(self.game_loop.category, "Случайная")

    @patch('src.game_loop.InputHandler')
    def test_post_game(self, mock_input_handler):
        """
        Тест проверяет действия после игры.
        """
        mock_input_handler.get_user_input.return_value = "2"
        with self.assertRaises(SystemExit):
            self.game_loop.post_game()

    def test_set_random_category_and_difficulty_if_needed(self):
        """
        Тест проверяет установку случайной категории и сложности,
        если это необходимо.
        """
        self.game_loop.set_random_category_and_difficulty_if_needed()
        self.assertNotEqual(self.game_loop.category, "Случайно")
        self.assertNotEqual(self.game_loop.difficulty, "Случайно")

    @patch('src.game_loop.sys')
    def test_exit_program(self, mock_sys):
        """
        Тест проверяет завершение программы.
        """
        mock_sys.exit.side_effect = SystemExit
        with self.assertRaises(SystemExit):
            self.game_loop.exit_program()
        mock_sys.exit.assert_called_once()

    @patch('src.game_loop.Renderer')
    def test_clear_screen_and_display_errors(self, mock_renderer):
        """
        Тест проверяет очистку экрана и отображение ошибок.
        """
        self.game_loop.clear_screen_and_display_errors()
        mock_renderer.clear_screen.assert_called_once()
        mock_renderer.display_error_if_exists.assert_called_once()

    @patch('src.game_loop.InputHandler')
    @patch('src.game_loop.GameLoop.handle_main_menu_choice')
    def test_run(self, mock_handle_main_menu_choice, mock_input_handler):
        """
        Тест проверяет выполнение цикла игры.
        """
        mock_input_handler.get_user_input.return_value = "1"  # "1" Начать игру
        mock_handle_main_menu_choice.side_effect = SystemExit
        with self.assertRaises(SystemExit):  # Ожидаем SystemExit exception
            self.game_loop.run()
        mock_handle_main_menu_choice.assert_called_once_with("1")

    @patch('src.game_loop.Renderer')
    @patch('src.game_loop.HangmanGame')
    @patch('src.game_loop.InputHandler')
    def test_start_game(self, mock_input_handler, mock_hangman_game,
                        mock_renderer):
        """
        Тест проверяет начало игры.
        """
        mock_game = MagicMock()
        mock_hangman_game.return_value = mock_game
        mock_game.is_game_over = False
        mock_input_handler.get_user_input.return_value = "4"  # Выход из игры

        try:
            self.game_loop.start_game()
        except SystemExit:
            pass

        mock_hangman_game.assert_called_once_with(self.word_dictionary,
                                                  self.game_loop.difficulty,
                                                  self.game_loop.category,
                                                  self.game_loop.error_handler)
        mock_game.reset_game.assert_called_once_with(self.game_loop.difficulty,
                                                     self.game_loop.category,
                                                     self.game_loop.error_handler)
        mock_renderer.assert_called_once_with(mock_game)
        mock_input_handler.get_user_input.assert_called_once_with(
            'Введите номер пункта меню или введите вашу букву: ')

    @patch('src.game_loop.GameLoop.choose_category')
    def test_choose_category(self, mock_choose_category):
        """
        Тест проверяет выбор категории.
        """
        self.game_loop.handle_main_menu_choice("2")
        mock_choose_category.assert_called_once()

    @patch('src.game_loop.GameLoop.choose_difficulty')
    def test_choose_difficulty(self, mock_choose_difficulty):
        """
        Тест проверяет выбор сложности.
        """
        self.game_loop.handle_main_menu_choice("3")
        mock_choose_difficulty.assert_called_once()

    @patch('src.game_loop.GameLoop.exit_program')
    def test_exit_program_from_menu(self, mock_exit_program):
        """
        Тест проверяет выбор завершения программы.
        """
        self.game_loop.handle_main_menu_choice("4")
        mock_exit_program.assert_called_once()

    @patch('src.game_loop.InputHandler.get_user_input',
           side_effect=['invalid', '1'])
    @patch('src.game_loop.Renderer.render_choose_option_menu')
    @patch('src.game_loop.GameLoop.clear_screen_and_display_errors')
    def test_choose_option_invalid_choice(self,
                                          mock_clear_screen_and_display_errors,
                                          mock_render_choose_option_menu,
                                          mock_get_user_input):
        """
        Тест проверяет choose_option с недопустимым выбором.
        """
        options = ['option1', 'option2', 'option3']
        self.game_loop.choose_option('test_option', options, 'category')

        self.assertEqual(mock_clear_screen_and_display_errors.call_count, 2)
        self.assertEqual(mock_render_choose_option_menu.call_count, 2)
        self.assertEqual(mock_get_user_input.call_count, 2)

        self.assertEqual(self.game_loop.category, 'option1')

    @patch('src.game_loop.InputHandler.get_user_input', return_value='1')
    @patch('src.game_loop.Renderer.render_choose_option_menu')
    @patch('src.game_loop.GameLoop.clear_screen_and_display_errors')
    def test_choose_option(self, mock_clear_screen_and_display_errors,
                           mock_render_choose_option_menu,
                           mock_get_user_input):
        """
        Тест метода choose_option.
        """
        options = ['option1', 'option2', 'option3']
        self.game_loop.choose_option('test_option', options, 'category')

        mock_clear_screen_and_display_errors.assert_called()
        mock_render_choose_option_menu.assert_called_with(options)
        mock_get_user_input.assert_called_with('Введите номер test_option: ')

        self.assertEqual(self.game_loop.category, 'option1')


if __name__ == '__main__':
    unittest.main()
