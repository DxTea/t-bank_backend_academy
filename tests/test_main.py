import unittest
from unittest.mock import patch
from src.main import main


class TestMainFunction(unittest.TestCase):

    @patch('src.main.Menu')
    def test_main(self, MockMenu):
        mock_menu_instance = MockMenu.return_value
        mock_menu_instance.main_menu.side_effect = [1, 3, StopIteration]

        with self.assertRaises(StopIteration):
            main()
        mock_menu_instance.welcome_screen.assert_called_once()
        self.assertEqual(mock_menu_instance.main_menu.call_count, 3)
        mock_menu_instance.handle_choice.assert_any_call(1)
        mock_menu_instance.handle_choice.assert_any_call(3)


if __name__ == '__main__':
    unittest.main()
