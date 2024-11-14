import argparse
import sys
import os
from datetime import datetime
from urllib.parse import urlparse
from typing import List, Optional


def parse_args() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    :return: Пространство имен с аргументами командной строки.
    """
    parser = argparse.ArgumentParser(description='Log Analyzer')
    parser.add_argument('--path', required='-i' not in sys.argv, nargs='+',
                        help='Path to log files or URLs')
    parser.add_argument('--from', dest='from_date',
                        help='Start date in format YYYY-MM-DD or '
                             'YYYY-MM-DDTHH:MM:SS')
    parser.add_argument('--to', dest='to_date',
                        help='End date in format YYYY-MM-DD or '
                             'YYYY-MM-DDTHH:MM:SS')
    parser.add_argument('--agent', help='Filter logs by user agent')
    parser.add_argument('--status_code', help='Filter logs by status code')
    parser.add_argument('--request_method',
                        help='Filter logs by request method')
    parser.add_argument('--general', action='store_true',
                        help='Generate general report')
    parser.add_argument('--format', choices=['md', 'adoc', 'json'],
                        default='md', help='Output format')
    parser.add_argument('-i', action='store_true',
                        help='Show program information')
    return parser.parse_args()


def format_date(date_str: Optional[str]) -> Optional[str]:
    """
    Форматирует строку даты в формат YYYY-MM-DDTHH:MM:SS.

    :param date_str: Строка даты.
    :return: Форматированная строка даты или None, если дата не указана.
    """
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').strftime(
                '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime(
                '%Y-%m-%dT00:00:00')
    return None


def validate_paths(paths: List[str]) -> bool:
    """
    Проверяет существование указанных путей.

    :param paths: Список путей к файлам или URL.
    :return: True, если все пути существуют, иначе False.
    """
    for path in paths:
        if not urlparse(path).scheme and not os.path.exists(path):
            print(f"Error: The file or directory '{path}' does not exist.")
            return False
    return True
