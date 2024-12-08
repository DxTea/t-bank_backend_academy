import os
import click
from typing import List
from tqdm import tqdm


def display_report_generation_status(parse_files_bar: tqdm,
                                     report_files_bar: tqdm,
                                     report_files: List[str]) -> None:
    """
    Отображает статус генерации отчетов и выводит список сгенерированных
    отчетов.

    :param parse_files_bar: Прогресс-бар для парсинга файлов.
    :param report_files_bar: Прогресс-бар для генерации отчетов.
    :param report_files: Список путей к сгенерированным отчетам.
    """
    parse_files_bar.colour = 'green'
    report_files_bar.colour = 'green'
    parse_files_bar.refresh()
    report_files_bar.refresh()
    parse_files_bar.close()
    report_files_bar.close()
    print('Reports generation completed!')

    if report_files:
        print('Generated reports:')
        for report_file in report_files:
            file_path = os.path.abspath(report_file)
            if os.name == 'nt':  # Windows
                click.echo(click.style(f'File "{file_path}"', fg='blue',
                                       underline=True))
            else:  # Linux, macOS
                print(
                    f'\033]8;;file://{file_path}\033\
                    \\{file_path}\033]8;;\033\\')


def show_program_info() -> None:
    """
    Отображает информацию о программе.
    """
    print(
        "Log Analyzer: Инструмент для анализа лог-файлов NGINX и генерации "
        "отчетов.")
    print("Версия: 1.1.0")
    print("Разработчик: Семён Давыдов aka DxTea")
    print(
        "Инструкция: список всех команд с пояснениями доступен по команде "
        "--help или -h")
    print("Лицензия: MIT")
