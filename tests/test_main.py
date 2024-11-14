import os
import sys
import unittest
from unittest.mock import patch, AsyncMock
import asyncio

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))

from src.main import main


class TestMain(unittest.TestCase):

    @patch('src.main.parse_args')
    @patch('src.main.show_program_info')
    @patch('src.main.validate_paths')
    @patch('src.main.generate_reports', new_callable=AsyncMock)
    def test_main_info(self, mock_generate_reports, mock_validate_paths,
                       mock_show_program_info, mock_parse_args):
        mock_parse_args.return_value = unittest.mock.Mock(i=True)
        asyncio.run(main())
        mock_show_program_info.assert_called_once()
        mock_generate_reports.assert_not_called()

    @patch('src.main.parse_args')
    @patch('src.main.show_program_info')
    @patch('src.main.validate_paths')
    @patch('src.main.generate_reports', new_callable=AsyncMock)
    def test_main_generate_reports(self, mock_generate_reports,
                                   mock_validate_paths, mock_show_program_info,
                                   mock_parse_args):
        mock_parse_args.return_value = unittest.mock.Mock(
            i=False,
            path='log_path',
            from_date='2021-01-01T00:00:00',
            to_date='2021-01-31T00:00:00',
            agent='agent',
            general='general',
            format='pdf',
            status_code='200',
            request_method='GET'
        )
        mock_validate_paths.return_value = True
        asyncio.run(main())
        mock_show_program_info.assert_not_called()
        mock_generate_reports.assert_called_once_with(
            'log_path', 'pdf', '2021-01-01T00:00:00', '2021-01-31T00:00:00',
            'agent', 'general', 200, 'GET'
        )

    @patch('src.main.parse_args')
    @patch('src.main.show_program_info')
    @patch('src.main.validate_paths')
    @patch('src.main.generate_reports', new_callable=AsyncMock)
    def test_main_invalid_paths(self, mock_generate_reports,
                                mock_validate_paths, mock_show_program_info,
                                mock_parse_args):
        mock_parse_args.return_value = unittest.mock.Mock(
            i=False,
            path='invalid_path',
            from_date='2021-01-01T00:00:00',
            to_date='2021-01-31T00:00:00',
            status_code='200'
        )
        mock_validate_paths.return_value = False
        asyncio.run(main())
        mock_show_program_info.assert_not_called()
        mock_generate_reports.assert_not_called()


if __name__ == '__main__':
    unittest.main()
