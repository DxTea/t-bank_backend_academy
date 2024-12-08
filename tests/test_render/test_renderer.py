import unittest
from unittest.mock import patch
from src.render.renderer import display_report_generation_status, \
    show_program_info
from tqdm import tqdm


class TestRenderer(unittest.TestCase):

    @patch('builtins.print')
    @patch('src.render.renderer.click')
    @patch('src.render.renderer.os')
    def test_display_report_generation_status(self, mock_os, mock_click,
                                              mock_print):
        parse_files_bar = tqdm(total=100, desc='Parsing files', position=0,
                               leave=True,
                               bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}]',
                               colour='red')
        report_files_bar = tqdm(total=1, desc='Generating reports', position=1,
                                leave=True,
                                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}]',
                                colour='blue')
        report_files = ['report1.html', 'report2.html']

        mock_os.name = 'nt'
        mock_os.path.abspath.side_effect = lambda x: f'C:\\path\\to\\{x}'

        display_report_generation_status(parse_files_bar, report_files_bar,
                                         report_files)

        self.assertEqual(parse_files_bar.colour, 'green')
        self.assertEqual(report_files_bar.colour, 'green')
        mock_print.assert_any_call('Reports generation completed!')
        mock_click.echo.assert_any_call(
            mock_click.style('File "C:\\path\\to\\report1.html"', fg='blue',
                             underline=True))
        mock_click.echo.assert_any_call(
            mock_click.style('File "C:\\path\\to\\report2.html"', fg='blue',
                             underline=True))

    @patch('builtins.print')
    def test_show_program_info(self, mock_print):
        show_program_info()

        mock_print.assert_any_call(
            "Log Analyzer: Инструмент для анализа лог-файлов NGINX и генерации отчетов.")
        mock_print.assert_any_call("Версия: 1.1.0")
        mock_print.assert_any_call("Разработчик: Семён Давыдов aka DxTea")
        mock_print.assert_any_call(
            "Инструкция: список всех команд с пояснениями доступен по команде --help или -h")
        mock_print.assert_any_call("Лицензия: MIT")


if __name__ == '__main__':
    unittest.main()
