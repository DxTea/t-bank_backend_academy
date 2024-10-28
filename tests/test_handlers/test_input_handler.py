import unittest
from unittest.mock import patch
from src.handlers.input_handler import InputHandler


class TestInputHandler(unittest.TestCase):

    @patch('builtins.input', return_value='1')
    def test_get_choice(self, mock_input):
        choice = InputHandler.get_choice("Enter your choice: ")
        self.assertEqual(choice, '1')
        mock_input.assert_called_once_with("Enter your choice: ")

    @patch('keyboard.is_pressed', side_effect=[False, False, True])
    def test_wait_for_space(self, mock_is_pressed):
        InputHandler.wait_for_space()
        self.assertEqual(mock_is_pressed.call_count, 3)
        mock_is_pressed.assert_called_with('space')

    @patch('builtins.input', side_effect=['0', '0'])
    @patch('random.randint', side_effect=[15, 18])
    def test_get_maze_size_random(self, mock_randint, mock_input):
        width, height = InputHandler.get_maze_size()
        self.assertEqual(width, 15)
        self.assertEqual(height, 18)
        mock_input.assert_any_call(
            "Введите внутреннюю ширину лабиринта (0 для случайного "
            "значения): ")
        mock_input.assert_any_call(
            "Введите внутреннюю высоту лабиринта (0 для случайного "
            "значения): ")
        mock_randint.assert_any_call(10, 20)

    @patch('builtins.input', side_effect=['12', '14'])
    def test_get_maze_size_specific(self, mock_input):
        width, height = InputHandler.get_maze_size()
        self.assertEqual(width, 12)
        self.assertEqual(height, 14)
        mock_input.assert_any_call(
            "Введите внутреннюю ширину лабиринта (0 для случайного "
            "значения): ")
        mock_input.assert_any_call(
            "Введите внутреннюю высоту лабиринта (0 для случайного "
            "значения): ")


if __name__ == '__main__':
    unittest.main()
