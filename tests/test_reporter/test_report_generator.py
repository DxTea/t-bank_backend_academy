import unittest
from unittest.mock import patch
from src.reporter.report_generator import generate_individual_reports, \
    generate_general_report, generate_reports, get_log_files
from src.reporter.reporter import Reporter
from tqdm import tqdm
import os


class TestReportGenerator(unittest.IsolatedAsyncioTestCase):

    @patch('src.reporter.report_generator.parse_logs')
    @patch('src.reporter.report_generator.analyze_logs')
    @patch('src.reporter.report_generator.Reporter.generate_report')
    async def test_generate_individual_reports(self, mock_generate_report,
                                               mock_analyze_logs,
                                               mock_parse_logs):
        log_files = ['log1.log', 'log2.log']
        reporter = Reporter(report_dir='reports')
        report_extension = 'json'
        from_date = '2023-01-01'
        to_date = '2023-01-31'
        agent = 'Mozilla/5.0'
        parse_files_bar = tqdm(total=len(log_files))
        report_files_bar = tqdm(total=len(log_files))

        mock_parse_logs.return_value = [{'log': 'data'}]
        mock_analyze_logs.return_value = {'analysis': 'result'}
        mock_generate_report.return_value = 'report.json'

        report_files = await generate_individual_reports(log_files, reporter,
                                                         report_extension,
                                                         from_date, to_date,
                                                         agent,
                                                         parse_files_bar,
                                                         report_files_bar)

        self.assertEqual(report_files, ['report.json', 'report.json'])
        self.assertEqual(report_files_bar.n, 2)

    @patch('src.reporter.report_generator.parse_logs')
    @patch('src.reporter.report_generator.analyze_logs')
    @patch('src.reporter.report_generator.Reporter.generate_report')
    async def test_generate_general_report(self, mock_generate_report,
                                           mock_analyze_logs, mock_parse_logs):
        log_files = ['log1.log', 'log2.log']
        reporter = Reporter(report_dir='reports')
        report_extension = 'json'
        from_date = '2023-01-01'
        to_date = '2023-01-31'
        agent = 'Mozilla/5.0'
        parse_files_bar = tqdm(total=len(log_files))
        report_files_bar = tqdm(total=1)

        mock_parse_logs.return_value = [{'log': 'data'}]
        mock_analyze_logs.return_value = {'analysis': 'result'}
        mock_generate_report.return_value = 'general_report.json'

        report_file = await generate_general_report(log_files, reporter,
                                                    report_extension,
                                                    from_date, to_date, agent,
                                                    parse_files_bar,
                                                    report_files_bar)

        self.assertEqual(report_file, 'general_report.json')
        self.assertEqual(report_files_bar.n, 1)

    @patch('src.reporter.report_generator.get_log_files')
    @patch('src.reporter.report_generator.create_progress_bars')
    @patch('src.reporter.report_generator.display_report_generation_status')
    @patch('src.reporter.report_generator.generate_individual_reports')
    @patch('src.reporter.report_generator.generate_general_report')
    async def test_generate_reports(self, mock_generate_general_report,
                                    mock_generate_individual_reports,
                                    mock_display_report_generation_status,
                                    mock_create_progress_bars,
                                    mock_get_log_files):
        log_source = 'logs'
        report_extension = 'json'
        from_date = '2023-01-01'
        to_date = '2023-01-31'
        agent = 'Mozilla/5.0'
        general = True

        mock_get_log_files.return_value = ['log1.log', 'log2.log']
        mock_create_progress_bars.return_value = (tqdm(total=2), tqdm(total=1))
        mock_generate_general_report.return_value = 'general_report.json'
        mock_generate_individual_reports.return_value = ['report1.json',
                                                         'report2.json']

        await generate_reports(log_source, report_extension, from_date,
                               to_date, agent, general)

        mock_get_log_files.assert_called_once_with(log_source)
        mock_create_progress_bars.assert_called_once_with(2, general)
        mock_generate_general_report.assert_called_once()
        mock_display_report_generation_status.assert_called_once()

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_get_log_files_with_list_of_directories(self, mock_walk,
                                                    mock_isdir):
        mock_isdir.side_effect = lambda x: x in ['dir1', 'dir2']
        mock_walk.side_effect = [
            [('dir1', [], ['file1.log', 'file2.txt', 'file3.csv'])],
            [('dir2', [], ['file4.log', 'file5.txt', 'file6.csv'])]
        ]
        log_source = ['dir1', 'dir2']
        expected = [
            os.path.join('dir1', 'file1.log'),
            os.path.join('dir1', 'file2.txt'),
            os.path.join('dir2', 'file4.log'),
            os.path.join('dir2', 'file5.txt')
        ]
        result = get_log_files(log_source)
        self.assertEqual(result, expected)

    @patch('os.path.isdir')
    def test_get_log_files_with_list_of_files(self, mock_isdir):
        mock_isdir.return_value = False
        log_source = ['file1.log', 'file2.txt']
        expected = ['file1.log', 'file2.txt']
        result = get_log_files(log_source)
        self.assertEqual(result, expected)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_get_log_files_with_single_directory(self, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('dir1', [], ['file1.log', 'file2.txt', 'file3.csv'])
        ]
        log_source = 'dir1'
        expected = [os.path.join('dir1', 'file1.log'),
                    os.path.join('dir1', 'file2.txt')]
        result = get_log_files(log_source)
        self.assertEqual(result, expected)

    @patch('os.path.isdir')
    def test_get_log_files_with_single_file(self, mock_isdir):
        mock_isdir.return_value = False
        log_source = 'file1.log'
        expected = ['file1.log']
        result = get_log_files(log_source)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
