import unittest
from src.reporter.report_formatter import MarkdownReportFormatter, \
    AsciiDocReportFormatter, JsonReportFormatter


class TestReportFormatter(unittest.TestCase):

    def setUp(self):
        self.analysis_result = {
            'total_requests': 100,
            'avg_size': 512,
            'p95_size': 1024,
            'max_size': 2048,
            'unique_ips': 10,
            'resources': {'/index.html': 50, '/about.html': 30},
            'statuses': {200: 80, 404: 20}
        }
        self.file_display_name = 'logfile.log'
        self.from_date = '2023-01-01'
        self.to_date = '2023-01-31'
        self.agent = 'Mozilla/5.0'

    def test_markdown_report_formatter(self):
        formatter = MarkdownReportFormatter()
        report = formatter.format(self.analysis_result, self.file_display_name,
                                  self.from_date, self.to_date, self.agent)
        self.assertIn('Общая информация', report)
        self.assertIn('Запрашиваемые ресурсы', report)
        self.assertIn('Коды ответа', report)

    def test_asciidoc_report_formatter(self):
        formatter = AsciiDocReportFormatter()
        report = formatter.format(self.analysis_result, self.file_display_name,
                                  self.from_date, self.to_date, self.agent)
        self.assertIn('Общая информация', report)
        self.assertIn('Запрашиваемые ресурсы', report)
        self.assertIn('Коды ответа', report)

    def test_json_report_formatter(self):
        formatter = JsonReportFormatter()
        report = formatter.format(self.analysis_result, self.file_display_name,
                                  self.from_date, self.to_date, self.agent)
        self.assertIn('"total_requests": 100', report)
        self.assertIn('"avg_size": 512', report)
        self.assertIn('"unique_ips": 10', report)


if __name__ == '__main__':
    unittest.main()
