import unittest
import os
from unittest.mock import patch, mock_open
from src.reporter.reporter import Reporter
from src.reporter.report_formatter import JsonReportFormatter, \
    MarkdownReportFormatter, AsciiDocReportFormatter


class TestReporter(unittest.TestCase):

    def setUp(self):
        self.reporter = Reporter(report_dir='reports')

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.reporter.reporter.JsonReportFormatter.format')
    def test_generate_report_json(self, mock_format, mock_open):
        mock_format.return_value = '{"key": "value"}'
        analysis_result = {'key': 'value'}
        file_path = 'logfile.log'
        report_extension = 'json'
        from_date = '2023-01-01'
        to_date = '2023-01-31'
        agent = 'Mozilla/5.0'

        report_filename = self.reporter.generate_report(file_path,
                                                        analysis_result,
                                                        report_extension,
                                                        from_date, to_date,
                                                        agent)

        expected_filename = os.path.join('reports', 'report_logfile.json')
        self.assertEqual(report_filename, expected_filename)
        mock_open.assert_called_once_with(expected_filename, 'w',
                                          encoding='utf-8')
        mock_format.assert_called_once_with(analysis_result, 'logfile.log',
                                            from_date, to_date, agent)

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.reporter.reporter.MarkdownReportFormatter.format')
    def test_generate_report_md(self, mock_format, mock_open):
        mock_format.return_value = '# Report'
        analysis_result = {'key': 'value'}
        file_path = 'logfile.log'
        report_extension = 'md'
        from_date = '2023-01-01'
        to_date = '2023-01-31'
        agent = 'Mozilla/5.0'

        report_filename = self.reporter.generate_report(file_path,
                                                        analysis_result,
                                                        report_extension,
                                                        from_date, to_date,
                                                        agent)

        expected_filename = os.path.join('reports', 'report_logfile.md')
        self.assertEqual(report_filename, expected_filename)
        mock_open.assert_called_once_with(expected_filename, 'w',
                                          encoding='utf-8')
        mock_format.assert_called_once_with(analysis_result, 'logfile.log',
                                            from_date, to_date, agent)

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.reporter.reporter.AsciiDocReportFormatter.format')
    def test_generate_report_adoc(self, mock_format, mock_open):
        mock_format.return_value = '= Report'
        analysis_result = {'key': 'value'}
        file_path = 'logfile.log'
        report_extension = 'adoc'
        from_date = '2023-01-01'
        to_date = '2023-01-31'
        agent = 'Mozilla/5.0'

        report_filename = self.reporter.generate_report(file_path,
                                                        analysis_result,
                                                        report_extension,
                                                        from_date, to_date,
                                                        agent)

        expected_filename = os.path.join('reports', 'report_logfile.adoc')
        self.assertEqual(report_filename, expected_filename)
        mock_open.assert_called_once_with(expected_filename, 'w',
                                          encoding='utf-8')
        mock_format.assert_called_once_with(analysis_result, 'logfile.log',
                                            from_date, to_date, agent)

    def test_get_formatter(self):
        self.assertIsInstance(self.reporter._get_formatter('json'),
                              JsonReportFormatter)
        self.assertIsInstance(self.reporter._get_formatter('md'),
                              MarkdownReportFormatter)
        self.assertIsInstance(self.reporter._get_formatter('adoc'),
                              AsciiDocReportFormatter)
        with self.assertRaises(ValueError):
            self.reporter._get_formatter('unsupported')


if __name__ == '__main__':
    unittest.main()
