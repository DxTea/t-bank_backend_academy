import unittest
import sys
from src.handlers.input_handler import parse_args, format_date, validate_paths
from unittest.mock import patch


class TestInputHandler(unittest.TestCase):

    def test_parse_args(self):
        test_args = ["program", "--path", "log1.txt", "--from", "2023-01-01",
                     "--to", "2023-01-31"]
        with patch.object(sys, 'argv', test_args):
            args = parse_args()
            self.assertEqual(args.path, ["log1.txt"])
            self.assertEqual(args.from_date, "2023-01-01")
            self.assertEqual(args.to_date, "2023-01-31")

    def test_format_date(self):
        test_cases = [
            ("2023-01-01T12:00:00", "2023-01-01T12:00:00"),
            ("2023-01-01", "2023-01-01T00:00:00"),
            (None, None)
        ]
        for date_str, expected in test_cases:
            with self.subTest(date_str=date_str, expected=expected):
                self.assertEqual(format_date(date_str), expected)

    def test_validate_paths(self):
        valid_paths = ["existing_file.txt"]
        invalid_paths = ["non_existing_file.txt"]

        with patch("os.path.exists", return_value=True):
            self.assertTrue(validate_paths(valid_paths))

        with patch("os.path.exists", return_value=False):
            self.assertFalse(validate_paths(invalid_paths))


if __name__ == '__main__':
    unittest.main()
