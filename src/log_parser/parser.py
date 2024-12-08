import aiofiles
import aiohttp
import re
from typing import List, Optional
from datetime import datetime, timezone
from urllib.parse import urlparse

from tqdm import tqdm

from src.models.log_record import LogRecord

log_pattern = re.compile(
    r'(?P<ip>\S+) - (?P<user>\S+) \[(?P<date>.*?)] "(?P<request>.*?)" ('
    r'?P<status>\d+) (?P<size>\d+) "(?P<referrer>.*?)" "(?P<agent>.*?)"'
)


async def fetch_logs_from_url(url: str) -> List[str]:
    """
    Загружает логи с указанного URL и возвращает их в виде списка строк.

    :param url: URL для загрузки логов.
    :return: Список строк логов.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.text()
            return content.splitlines()


async def read_log_file(file_path: str) -> List[str]:
    """
    Читает файл логов и возвращает его содержимое в виде списка строк.

    :param file_path: Путь к файлу логов.
    :return: Список строк логов.
    """
    async with aiofiles.open(file_path, 'r') as f:
        return [line async for line in f]


def parse_log_line(line: str) -> Optional[LogRecord]:
    """
    Парсит строку лога и возвращает объект LogRecord.

    :param line: Строка лога.
    :return: Объект LogRecord или None, если строка не соответствует шаблону.
    """
    match = log_pattern.match(line)
    if match:
        log_dict = match.groupdict()
        log_date = datetime.strptime(log_dict['date'],
                                     '%d/%b/%Y:%H:%M:%S %z').astimezone(
            timezone.utc).isoformat()
        return LogRecord(
            ip=log_dict['ip'],
            user=log_dict['user'],
            date=log_date,
            request=log_dict['request'],
            status=int(log_dict['status']),
            size=int(log_dict['size']),
            referrer=log_dict['referrer'],
            agent=log_dict['agent']
        )
    return None


async def parse_log_file(file_path: str,
                         from_date: Optional[str] = None,
                         to_date: Optional[str] = None,
                         agent: Optional[str] = None,
                         status_code: Optional[int] = None,
                         request_method:
                         Optional[str] = None) -> List[LogRecord]:
    """
    Парсит файл логов и возвращает список записей логов.

    :param file_path: Путь к файлу логов.
    :param from_date: Начальная дата для фильтрации логов (опционально).
    :param to_date: Конечная дата для фильтрации логов (опционально).
    :param agent: User-Agent для фильтрации логов (опционально).
    :param status_code: Код статуса для фильтрации логов (опционально).
    :param request_method: Метод запроса для фильтрации логов (опционально).
    :return: Список записей логов.
    """
    if urlparse(file_path).scheme in ('http', 'https'):
        lines = await fetch_logs_from_url(file_path)
    else:
        lines = await read_log_file(file_path)

    logs: List[LogRecord] = []
    for line in lines:
        log = parse_log_line(line)
        conditions = [
            not from_date or log.date >= from_date,
            not to_date or log.date <= to_date,
            not agent or agent in log.agent,
            not status_code or log.status == status_code,
            not request_method or log.request.lower().startswith(
                request_method.lower())
        ]

        if log and all(conditions):
            logs.append(log)
    return logs


async def parse_logs(log_files: List[str], from_date: Optional[str] = None,
                     to_date: Optional[str] = None,
                     agent: Optional[str] = None,
                     parse_files_bar: Optional[tqdm] = None,
                     status_code: Optional[int] = None,
                     request_method: Optional[str] = None) -> List[LogRecord]:
    """
    Парсит файлы логов и возвращает список записей логов.

    :param log_files: Список путей к файлам логов.
    :param from_date: Начальная дата для фильтрации логов (опционально).
    :param to_date: Конечная дата для фильтрации логов (опционально).
    :param agent: User-Agent для фильтрации логов (опционально).
    :param parse_files_bar: Прогресс-бар для парсинга файлов (опционально).
    :param status_code: Код статуса для фильтрации логов (опционально).
    :param request_method: Метод запроса для фильтрации логов (опционально).
    :return: Список записей логов.
    """
    all_logs: List[LogRecord] = []
    for file in log_files:
        logs = await parse_log_file(file, from_date, to_date, agent,
                                    status_code, request_method)
        all_logs.extend(logs)
        if parse_files_bar:
            parse_files_bar.update(1)
    return all_logs
