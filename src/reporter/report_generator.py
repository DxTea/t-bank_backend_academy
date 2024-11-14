import os
from typing import Optional, List, Union

from src.log_analyzer.analyzer import analyze_logs
from src.log_parser.parser import parse_logs
from src.render.progress_bar import create_progress_bars
from src.render.renderer import display_report_generation_status
from src.reporter.reporter import Reporter


def get_log_files(log_source: Union[str, List[str]]) -> List[str]:
    """
    Возвращает список файлов логов из указанного источника.

    :param log_source: Путь к файлу или директории с логами, либо список
    таких путей.
    :return: Список путей к файлам логов.
    """
    if isinstance(log_source, list):
        log_files = []
        for source in log_source:
            if os.path.isdir(source):
                log_files.extend([os.path.join(root, file)
                                  for root, _, files in os.walk(source)
                                  for file in files if
                                  file.endswith(('.log', '.txt'))])
            else:
                log_files.append(source)
        return log_files
    else:
        if os.path.isdir(log_source):
            return [os.path.join(root, file)
                    for root, _, files in os.walk(log_source)
                    for file in files if file.endswith(('.log', '.txt'))]
        return [log_source]


async def generate_individual_reports(log_files: List[str], reporter: Reporter,
                                      report_extension: str,
                                      from_date: Optional[str],
                                      to_date: Optional[str],
                                      agent: Optional[str],
                                      parse_files_bar=None,
                                      report_files_bar=None,
                                      status_code: Optional[int] = None,
                                      request_method: Optional[str] = None) \
        -> List[str]:
    """
    Генерирует индивидуальные отчеты для каждого файла логов.

    :param log_files: Список путей к файлам логов.
    :param reporter: Объект Reporter для генерации отчетов.
    :param report_extension: Расширение файла отчета (md, adoc, json).
    :param from_date: Начальная дата для фильтрации логов (опционально).
    :param to_date: Конечная дата для фильтрации логов (опционально).
    :param agent: User-Agent для фильтрации логов (опционально).
    :param parse_files_bar: Прогресс-бар для парсинга файлов (опционально).
    :param report_files_bar: Прогресс-бар для генерации отчетов (опционально).
    :param status_code: Код статуса для фильтрации логов (опционально).
    :param request_method: Метод запроса для фильтрации логов (опционально).
    :return: Список путей к сгенерированным отчетам.
    """
    report_files = []

    for file in log_files:
        logs = await parse_logs([file], from_date, to_date, agent,
                                parse_files_bar, status_code, request_method)
        analysis_result = await analyze_logs(logs)
        report_file = reporter.generate_report(file, analysis_result,
                                               report_extension, from_date,
                                               to_date, agent, general=False)
        report_files.append(report_file)
        if report_files_bar:
            report_files_bar.update(1)
    return report_files


async def generate_general_report(log_files: List[str], reporter: Reporter,
                                  report_extension: str,
                                  from_date: Optional[str],
                                  to_date: Optional[str], agent: Optional[str],
                                  parse_files_bar=None,
                                  report_files_bar=None,
                                  status_code: Optional[int] = None,
                                  request_method: Optional[str] = None) -> str:
    """
    Генерирует общий отчет для всех файлов логов.

    :param log_files: Список путей к файлам логов.
    :param reporter: Объект Reporter для генерации отчетов.
    :param report_extension: Расширение файла отчета (md, adoc, json).
    :param from_date: Начальная дата для фильтрации логов (опционально).
    :param to_date: Конечная дата для фильтрации логов (опционально).
    :param agent: User-Agent для фильтрации логов (опционально).
    :param parse_files_bar: Прогресс-бар для парсинга файлов (опционально).
    :param report_files_bar: Прогресс-бар для генерации отчетов (опционально).
    :param status_code: Код статуса для фильтрации логов (опционально).
    :param request_method: Метод запроса для фильтрации логов (опционально).
    :return: Путь к сгенерированному общему отчету.
    """
    all_logs = await parse_logs(log_files, from_date, to_date, agent,
                                parse_files_bar, status_code, request_method)
    analysis_result = await analyze_logs(all_logs)
    if report_files_bar:
        report_files_bar.update(1)
    return reporter.generate_report(log_files, analysis_result,
                                    report_extension, from_date, to_date,
                                    agent, general=True)


async def generate_reports(log_source: Union[str, List[str]],
                           report_extension: Optional[str] = 'md',
                           from_date: Optional[str] = None,
                           to_date: Optional[str] = None,
                           agent: Optional[str] = None,
                           general: bool = False,
                           status_code: Optional[int] = None,
                           request_method: Optional[str] = None) -> None:
    """
    Генерирует отчеты на основе логов из указанного источника.

    :param log_source: Путь к файлу или директории с логами, либо список
    таких путей.
    :param report_extension: Расширение файла отчета (md, adoc, json).
    :param from_date: Начальная дата для фильтрации логов (опционально).
    :param to_date: Конечная дата для фильтрации логов (опционально).
    :param agent: User-Agent для фильтрации логов (опционально).
    :param general: Флаг для генерации общего отчета.
    :param status_code: Код статуса для фильтрации логов (опционально).
    :param request_method: Метод запроса для фильтрации логов (опционально).
    """
    log_files = get_log_files(log_source)
    if not log_files:
        return

    parse_files_bar, report_files_bar = create_progress_bars(len(log_files),
                                                             general)

    reports_dir = 'reports'
    os.makedirs(reports_dir, exist_ok=True)
    reporter = Reporter(report_dir=reports_dir)

    report_files = []
    if general:
        report_file = await generate_general_report(log_files, reporter,
                                                    report_extension,
                                                    from_date, to_date, agent,
                                                    parse_files_bar,
                                                    report_files_bar,
                                                    status_code,
                                                    request_method)
        report_files.append(report_file)
    else:
        report_files = await generate_individual_reports(log_files, reporter,
                                                         report_extension,
                                                         from_date, to_date,
                                                         agent,
                                                         parse_files_bar,
                                                         report_files_bar,
                                                         status_code,
                                                         request_method)

    display_report_generation_status(parse_files_bar, report_files_bar,
                                     report_files)
