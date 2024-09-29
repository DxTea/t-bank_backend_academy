from unittest.mock import patch
from src.main import main


def test_main() -> None:
    with patch('builtins.input', return_value='any'):
        with patch('src.main.GameLoop.run', return_value=None):
            main()
