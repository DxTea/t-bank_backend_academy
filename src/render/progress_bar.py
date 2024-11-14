from tqdm import tqdm
from typing import Tuple


def create_progress_bar(total: int, desc: str, bar_color: str,
                        position: int) -> tqdm:
    """
    Создает индикатор выполнения с указанным цветом и позицией.

    :param total: Общее количество итераций.
    :param desc: Описание индикатора выполнения.
    :param bar_color: Цвет индикатора выполнения.
    :param position: Позиция индикатора выполнения в консоли.
    :return: Экземпляр индикатора выполнения tqdm.
    """
    return tqdm(total=total, desc=desc, position=position, leave=True,
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}, '
                           '{rate_fmt}]',
                colour=bar_color)


def create_progress_bars(log_files_len: int,
                         general: bool) -> Tuple[tqdm, tqdm]:
    """
    Создает индикаторы выполнения для парсинга файлов и генерации отчетов.

    :param log_files_len: Количество лог-файлов.
    :param general: Флаг, указывающий на генерацию общего отчета.
    :return: Кортеж из двух индикаторов выполнения tqdm.
    """
    parse_files_bar = create_progress_bar(log_files_len, 'Parsing files',
                                          bar_color='red', position=0)
    report_files_bar = create_progress_bar(1 if general else log_files_len,
                                           'Generating reports',
                                           bar_color='blue', position=1)
    return parse_files_bar, report_files_bar
