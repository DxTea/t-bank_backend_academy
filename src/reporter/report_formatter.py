import json
from http import HTTPStatus
from typing import Dict, Optional


class ReportFormatter:
    def format(self, analysis_result: Dict, file_display_name: str,
               from_date: Optional[str], to_date: Optional[str],
               agent: Optional[str]) -> str:
        """
        Форматирует результаты анализа в строку отчета.

        :param analysis_result: Результаты анализа в виде словаря.
        :param file_display_name: Имя файла для отображения в отчете.
        :param from_date: Начальная дата анализа.
        :param to_date: Конечная дата анализа.
        :param agent: Информация об агенте.
        :return: Отформатированный отчет в виде строки.
        """
        raise NotImplementedError

    def _get_status_name(self, code: int) -> str:
        """
        Возвращает имя статуса по коду.

        :param code: Код статуса.
        :return: Имя статуса.
        """
        try:
            return HTTPStatus(code).phrase
        except ValueError:
            return 'Unknown Status'


class MarkdownReportFormatter(ReportFormatter):
    def format(self, analysis_result: Dict, file_display_name: str,
               from_date: Optional[str], to_date: Optional[str],
               agent: Optional[str] = None) -> str:
        """
        Форматирует результаты анализа в отчет в формате Markdown.

        :param analysis_result: Результаты анализа в виде словаря.
        :param file_display_name: Имя файла для отображения в отчете.
        :param from_date: Начальная дата анализа.
        :param to_date: Конечная дата анализа.
        :param agent: Информация об агенте.
        :return: Отчет в формате Markdown.
        """
        agent_info = f"|       Агент        |   {agent} |\n" if agent else ""
        return f"""
#### Общая информация

|        Метрика        |     Значение |
|:---------------------:|-------------:|
|       Файл(-ы)        | `{file_display_name}` |
|    Начальная дата     |   {from_date or '-'} |
|     Конечная дата     |   {to_date or '-'} |
|  Количество запросов  |       {analysis_result['total_requests']} |
| Средний размер ответа |         {analysis_result['avg_size']}b |
|  95p размера ответа   |         {analysis_result['p95_size']}b |
| Максимальный размер ответа |         {analysis_result['max_size']}b |
| Уникальные IP-адреса  |       {analysis_result['unique_ips']} |
{agent_info}
#### Запрашиваемые ресурсы

|     Ресурс      | Количество |
|:---------------:|-----------:|
{self._format_resources_md(analysis_result['resources'])}

#### Коды ответа

| Код |          Имя          | Количество |
|:---:|:---------------------:|-----------:|
{self._format_statuses_md(analysis_result['statuses'])}
"""

    def _format_resources_md(self, resources: Dict) -> str:
        """
        Форматирует ресурсы в таблицу Markdown.

        :param resources: Словарь ресурсов и их количества.
        :return: Таблица ресурсов в формате Markdown.
        """
        return '\n'.join(
            [f"|  `{resource}`  |      {count} |" for resource, count in
             resources.items()])

    def _format_statuses_md(self, statuses: Dict) -> str:
        """
        Форматирует коды статусов в таблицу Markdown.

        :param statuses: Словарь кодов статусов и их количества.
        :return: Таблица кодов статусов в формате Markdown.
        """
        return '\n'.join([
            f"|  {code} |          {self._get_status_name(code)}          |       {count} |"
            for code, count in statuses.items()])


class AsciiDocReportFormatter(ReportFormatter):
    def format(self, analysis_result: Dict, file_display_name: str,
               from_date: Optional[str], to_date: Optional[str],
               agent: Optional[str] = None) -> str:
        """
        Форматирует результаты анализа в отчет в формате AsciiDoc.

        :param analysis_result: Результаты анализа в виде словаря.
        :param file_display_name: Имя файла для отображения в отчете.
        :param from_date: Начальная дата анализа.
        :param to_date: Конечная дата анализа.
        :param agent: Информация об агенте.
        :return: Отчет в формате AsciiDoc.
        """
        agent_info = f"| Агент | {agent}\n" if agent else ""
        return f"""
== Общая информация

[cols="2,1", options="header"]
|===
| Метрика | Значение
| Файл(-ы) | `{file_display_name}`
| Начальная дата | {from_date or '-'}
| Конечная дата | {to_date or '-'}
| Количество запросов | {analysis_result['total_requests']}
| Средний размер ответа | {analysis_result['avg_size']}b
| 95p размера ответа | {analysis_result['p95_size']}b
| Максимальный размер ответа | {analysis_result['max_size']}b
| Уникальные IP-адреса | {analysis_result['unique_ips']}
{agent_info}|===

== Запрашиваемые ресурсы

[cols="2,1", options="header"]
|===
| Ресурс | Количество
{self._format_resources_adoc(analysis_result['resources'])}
|===

== Коды ответа

[cols="1,2,3", options="header"]
|===
| Код | Имя | Количество
{self._format_statuses_adoc(analysis_result['statuses'])}
|===
"""

    def _format_resources_adoc(self, resources: Dict) -> str:
        """
        Форматирует ресурсы в таблицу AsciiDoc.

        :param resources: Словарь ресурсов и их количества.
        :return: Таблица ресурсов в формате AsciiDoc.
        """
        return '\n'.join([f'| `{resource}` | {count}' for resource, count in
                          resources.items()])

    def _format_statuses_adoc(self, statuses: Dict) -> str:
        """
        Форматирует коды статусов в таблицу AsciiDoc.

        :param statuses: Словарь кодов статусов и их количества.
        :return: Таблица кодов статусов в формате AsciiDoc.
        """
        return '\n'.join(
            [f'| {code} | {self._get_status_name(code)} | {count}' for
             code, count in statuses.items()])


class JsonReportFormatter(ReportFormatter):
    def format(self, analysis_result: Dict, file_display_name: str,
               from_date: Optional[str], to_date: Optional[str],
               agent: Optional[str]) -> str:
        """
        Форматирует результаты анализа в отчет в формате JSON.

        :param analysis_result: Результаты анализа в виде словаря.
        :param file_display_name: Имя файла для отображения в отчете.
        :param from_date: Начальная дата анализа.
        :param to_date: Конечная дата анализа.
        :param agent: Информация об агенте.
        :return: Отчет в формате JSON.
        """
        return json.dumps(analysis_result, ensure_ascii=False, indent=4)
