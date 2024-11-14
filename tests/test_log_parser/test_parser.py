import unittest
from unittest.mock import patch, AsyncMock
from src.log_parser.parser import parse_log_file, \
    parse_log_line, parse_logs
from src.models.log_record import LogRecord


class TestParser(unittest.IsolatedAsyncioTestCase):

    def test_parse_log_line_none(self):
        line = 'invalid log line'
        result = parse_log_line(line)
        self.assertIsNone(result)

    @patch('src.log_parser.parser.read_log_file', new_callable=AsyncMock)
    async def test_parse_log_file(self, mock_read_log_file):
        mock_read_log_file.return_value = [
            '127.0.0.1 - user [01/Jan/2023:00:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234 "http://example.com" "Mozilla/5.0"'
        ]
        file_path = 'test.log'
        result = await parse_log_file(file_path)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ip, '127.0.0.1')

    @patch('src.log_parser.parser.parse_log_file', new_callable=AsyncMock)
    async def test_parse_logs_with_continue(self, mock_parse_log_file):
        mock_parse_log_file.return_value = [
            LogRecord(
                ip='127.0.0.1',
                user='user',
                date='2023-01-01T00:00:00+00:00',
                request='GET /index.html HTTP/1.1',
                status=200,
                size=1234,
                referrer='http://example.com',
                agent='Mozilla/5.0'
            )
        ]
        log_files = ['test.log']
        result = await parse_logs(log_files,
                                  from_date='2023-01-02T00:00:00+00:00')
        self.assertEqual(len(result), 1)

    @patch('tqdm.tqdm')
    @patch('src.log_parser.parser.parse_log_file', new_callable=AsyncMock)
    async def test_parse_logs_with_progress_bar(self, mock_parse_log_file,
                                                mock_tqdm):
        mock_parse_log_file.return_value = []
        mock_update = mock_tqdm.return_value
        log_files = ['test.log']
        await parse_logs(log_files, parse_files_bar=mock_update)
        mock_update.update.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
