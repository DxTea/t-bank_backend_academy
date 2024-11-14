import os
from typing import Optional, Dict, Union

from src.reporter.report_formatter import ReportFormatter, \
    MarkdownReportFormatter, AsciiDocReportFormatter, JsonReportFormatter


class Reporter:
    def __init__(self, report_dir: str = 'reports') -> None:
        """
        Инициализирует объект Reporter.

        :param report_dir: Директория для сохранения отчетов.
        """
        self.report_dir = report_dir

    def generate_report(self, file_path: Union[str, list],
                        analysis_result: Dict,
                        report_extension: str,
                        from_date: Optional[str] = None,
                        to_date: Optional[str] = None,
                        agent: Optional[str] = None,
                        general: bool = False) -> str:
        """
        Генерирует отчет на основе результатов анализа.

        :param file_path: Путь к файлу или список файлов для анализа.
        :param analysis_result: Результаты анализа в виде словаря.
        :param report_extension: Расширение файла отчета (md, adoc, json).
        :param from_date: Начальная дата анализа.
        :param to_date: Конечная дата анализа.
        :param agent: Информация об агенте.
        :param general: Флаг для генерации общего отчета.
        :return: Путь к сгенерированному отчету.
        """
        if general:
            sanitized_filename = "general"
            file_display_name = ', '.join(
                [os.path.basename(f) for f in file_path]) if isinstance(
                file_path, list) else os.path.basename(file_path)
        else:
            sanitized_filename = os.path.splitext(os.path.basename(file_path))[
                0].replace('\\', '_').replace('/', '_')
            file_display_name = os.path.basename(file_path)

        report_filename = os.path.join(self.report_dir,
                                       f'report_{sanitized_filename}.'
                                       f'{report_extension}')
        formatter = self._get_formatter(report_extension)
        report_content = formatter.format(analysis_result,
                                          str(file_display_name),
                                          from_date, to_date, agent)

        with open(report_filename, 'w', encoding='utf-8') as report_file:
            report_file.write(report_content)
        return report_filename

    def _get_formatter(self, report_extension: str) -> ReportFormatter:
        """
        Возвращает соответствующий форматтер для отчета.

        :param report_extension: Расширение файла отчета (md, adoc, json).
        :return: Объект форматтера.
        :raises ValueError: Если расширение отчета не поддерживается.
        """
        if report_extension == 'md':
            return MarkdownReportFormatter()
        elif report_extension == 'adoc':
            return AsciiDocReportFormatter()
        elif report_extension == 'json':
            return JsonReportFormatter()
        else:
            raise ValueError(
                f'Unsupported report extension: {report_extension}')
