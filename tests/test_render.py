import unittest
from unittest.mock import patch, MagicMock
from src.hangman_game import HangmanGame
from src.word import Word
from src.render import Renderer


class TestRenderer(unittest.TestCase):
    def setUp(self):
        """
        Метод для установки начальных условий перед каждым тестом.
        """
        self.game = MagicMock(spec=HangmanGame)
        self.game.remaining_attempts = 5
        self.game.guessed_letters = set()
        self.game.current_word = MagicMock()
        self.game.current_word.word = "test"
        self.renderer = Renderer(self.game)

    @patch('builtins.print')
    def test_render_game(self, mock_print):
        """
        Тест проверяет отображение текущего состояния игры.
        """
        self.renderer.render_game()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_render_game_result(self, mock_print):
        """
        Тест проверяет отображение результата игры.
        """
        Renderer.render_game_result(self.game)
        mock_print.assert_called()

    @patch('builtins.print')
    def test_view_word(self, mock_print):
        """
        Тест проверяет просмотр слова.
        """
        word = Word("тест", "подсказка1", "подсказка2", "категория")
        Renderer.view_word(word)
        mock_print.assert_called()

    @patch('builtins.print')
    def test_render_main_menu(self, mock_print):
        """
        Тест проверяет отображение главного меню.
        """
        Renderer.render_main_menu("Случайная", "Случайно")
        mock_print.assert_called()

    @patch('builtins.print')
    def test_render_game_menu(self, mock_print):
        """
        Тест проверяет отображение меню игры.
        """
        Renderer.render_game_menu(["1. Подсказка 1", "2. Подсказка 2"])
        mock_print.assert_called()

    @patch('builtins.print')
    def test_render_post_game_menu(self, mock_print):
        """
        Тест проверяет отображение меню после игры.
        """
        Renderer.render_post_game_menu()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_render_choose_option_menu(self, mock_print):
        """
        Тест проверяет отображение меню выбора опции.
        """
        Renderer.render_choose_option_menu(["1. Опция 1", "2. Опция 2"])
        mock_print.assert_called()

    @patch('os.system')
    def test_clear_screen(self, mock_system):
        """
        Тест проверяет очистку экрана.
        """
        Renderer.clear_screen()
        mock_system.assert_called()

    @patch('builtins.print')
    def test_display_error_if_exists(self, mock_print):
        """
        Тест проверяет отображение ошибки, если она существует.
        """
        Renderer.display_error_if_exists("Тестовая ошибка")
        mock_print.assert_called()

    @patch('builtins.print')
    def test_used_letters(self, mock_print):
        """
        Тест проверяет свойство used_letters.
        """
        self.game.guessed_letters = {'т', 'с'}
        renderer = Renderer(self.game)
        self.assertEqual(set(renderer.used_letters.split(', ')),
                         self.game.guessed_letters)


if __name__ == '__main__':
    unittest.main()
