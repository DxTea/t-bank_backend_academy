import unittest
from unittest.mock import patch
from src.input_handler import InputHandler
from src.custom_errors import InvalidMenuChoiceError, InvalidUserGuessError, \
    HintUsageError


class TestInputHandler(unittest.TestCase):
    @patch('builtins.input', return_value='1')
    def test_get_user_input(self, mock_input):
        """
        Тест проверяет получение ввода пользователя.
        """
        result = InputHandler.get_user_input("Введите номер: ")
        self.assertEqual(result, '1')
        mock_input.assert_called_once_with("Введите номер: ")

    def test_validate_menu_choice_valid(self):
        """
        Тест проверяет валидацию выбора пользователя в меню с валидным выбором.
        """
        result = InputHandler.validate_menu_choice('1', ['1', '2', '3'])
        self.assertEqual(result, '1')

    def test_validate_menu_choice_invalid(self):
        """
        Тест проверяет валидацию выбора пользователя в меню
        с невалидным выбором.
        """
        with self.assertRaises(InvalidMenuChoiceError):
            InputHandler.validate_menu_choice('4', ['1', '2', '3'])

    def test_validate_user_guess_valid(self):
        """
        Тест проверяет валидацию предположения пользователя
        с валидным предположением.
        """
        result = InputHandler.validate_user_guess('a')
        self.assertEqual(result, 'a')

    def test_validate_user_guess_invalid(self):
        """
        Тест проверяет валидацию предположения пользователя
        с невалидным предположением.
        """
        with self.assertRaises(InvalidUserGuessError):
            InputHandler.validate_user_guess('ab')

    def test_validate_hint_usage_valid(self):
        """
        Тест проверяет валидацию использования подсказки
        с валидным использованием.
        """
        InputHandler.validate_hint_usage(0,
                                         ["1. Подсказка 1", "2. Подсказка 2"])

    def test_validate_hint_usage_invalid(self):
        """
        Тест проверяет валидацию использования подсказки
        с невалидным использованием.
        """
        with self.assertRaises(HintUsageError):
            InputHandler.validate_hint_usage(0, ["Подсказка 1: Test hint",
                                                 "2. Подсказка 2"])


if __name__ == '__main__':
    unittest.main()
