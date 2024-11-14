import unittest
from unittest.mock import patch
from src.render.progress_bar import create_progress_bar, create_progress_bars
from tqdm import tqdm


class TestProgressBar(unittest.TestCase):

    @patch('src.render.progress_bar.tqdm')
    def test_create_progress_bar(self, mock_tqdm):
        total = 100
        desc = 'Test Progress'
        bar_color = 'green'
        position = 0

        # Set the return value of the tqdm mock to be an instance of tqdm
        mock_tqdm.return_value = tqdm(total=total, desc=desc,
                                      position=position, leave=True,
                                      bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}]',
                                      colour=bar_color)

        progress_bar = create_progress_bar(total, desc, bar_color, position)

        mock_tqdm.assert_called_once_with(
            total=total,
            desc=desc,
            position=position,
            leave=True,
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}]',
            colour=bar_color
        )
        self.assertIsInstance(progress_bar, tqdm)

    @patch('src.render.progress_bar.create_progress_bar')
    def test_create_progress_bars(self, mock_create_progress_bar):
        log_files_len = 5
        general = True

        parse_files_bar, report_files_bar = create_progress_bars(log_files_len,
                                                                 general)

        self.assertEqual(mock_create_progress_bar.call_count, 2)
        mock_create_progress_bar.assert_any_call(log_files_len,
                                                 'Parsing files',
                                                 bar_color='red', position=0)
        mock_create_progress_bar.assert_any_call(1, 'Generating reports',
                                                 bar_color='blue', position=1)

        general = False
        parse_files_bar, report_files_bar = create_progress_bars(log_files_len,
                                                                 general)

        self.assertEqual(mock_create_progress_bar.call_count, 4)
        mock_create_progress_bar.assert_any_call(log_files_len,
                                                 'Parsing files',
                                                 bar_color='red', position=0)
        mock_create_progress_bar.assert_any_call(log_files_len,
                                                 'Generating reports',
                                                 bar_color='blue', position=1)


if __name__ == '__main__':
    unittest.main()
