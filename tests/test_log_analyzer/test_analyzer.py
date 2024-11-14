import unittest
from collections import Counter
from src.log_analyzer.analyzer import analyze_logs
from src.models.log_record import LogRecord
import numpy as np


class TestAnalyzer(unittest.IsolatedAsyncioTestCase):

    async def test_analyze_logs_empty(self):
        logs = []
        result = await analyze_logs(logs)
        expected = {
            'total_requests': 0,
            'resources': Counter(),
            'statuses': Counter(),
            'avg_size': 0.0,
            'p95_size': 0.0,
            'max_size': 0,
            'unique_ips': 0
        }
        self.assertEqual(result, expected)

    async def test_analyze_logs(self):
        logs = [
            LogRecord(
                ip='127.0.0.1',
                user='user1',
                date='2023-01-01T00:00:00+00:00',
                request='GET /index.html HTTP/1.1',
                status=200,
                size=1234,
                referrer='http://example.com',
                agent='Mozilla/5.0'
            ),
            LogRecord(
                ip='127.0.0.2',
                user='user2',
                date='2023-01-01T00:01:00+00:00',
                request='POST /form HTTP/1.1',
                status=404,
                size=5678,
                referrer='http://example.com',
                agent='Mozilla/5.0'
            )
        ]
        result = await analyze_logs(logs)
        expected = {
            'total_requests': 2,
            'resources': Counter(
                {'GET /index.html HTTP/1.1': 1, 'POST /form HTTP/1.1': 1}),
            'statuses': Counter({200: 1, 404: 1}),
            'avg_size': 3456.0,
            'p95_size': float(np.percentile([1234, 5678], 95)),
            'max_size': 5678,
            'unique_ips': 2
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
