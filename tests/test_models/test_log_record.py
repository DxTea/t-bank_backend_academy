import unittest
from src.models.log_record import LogRecord


class TestLogRecord(unittest.TestCase):

    def test_log_record_initialization(self):
        log_record = LogRecord(
            ip="127.0.0.1",
            user="user1",
            date="2023-01-01T00:00:00+00:00",
            request="GET /index.html HTTP/1.1",
            status=200,
            size=1024,
            referrer="http://example.com",
            agent="Mozilla/5.0"
        )
        self.assertEqual(log_record.ip, "127.0.0.1")
        self.assertEqual(log_record.user, "user1")
        self.assertEqual(log_record.date, "2023-01-01T00:00:00+00:00")
        self.assertEqual(log_record.request, "GET /index.html HTTP/1.1")
        self.assertEqual(log_record.status, 200)
        self.assertEqual(log_record.size, 1024)
        self.assertEqual(log_record.referrer, "http://example.com")
        self.assertEqual(log_record.agent, "Mozilla/5.0")

    def test_log_record_equality(self):
        log_record1 = LogRecord(
            ip="127.0.0.1",
            user="user1",
            date="2023-01-01T00:00:00+00:00",
            request="GET /index.html HTTP/1.1",
            status=200,
            size=1024,
            referrer="http://example.com",
            agent="Mozilla/5.0"
        )
        log_record2 = LogRecord(
            ip="127.0.0.1",
            user="user1",
            date="2023-01-01T00:00:00+00:00",
            request="GET /index.html HTTP/1.1",
            status=200,
            size=1024,
            referrer="http://example.com",
            agent="Mozilla/5.0"
        )
        self.assertEqual(log_record1.ip, log_record2.ip)
        self.assertEqual(log_record1.user, log_record2.user)
        self.assertEqual(log_record1.date, log_record2.date)
        self.assertEqual(log_record1.request, log_record2.request)
        self.assertEqual(log_record1.status, log_record2.status)
        self.assertEqual(log_record1.size, log_record2.size)
        self.assertEqual(log_record1.referrer, log_record2.referrer)
        self.assertEqual(log_record1.agent, log_record2.agent)

    def test_log_record_inequality(self):
        log_record1 = LogRecord(
            ip="127.0.0.1",
            user="user1",
            date="2023-01-01T00:00:00+00:00",
            request="GET /index.html HTTP/1.1",
            status=200,
            size=1024,
            referrer="http://example.com",
            agent="Mozilla/5.0"
        )
        log_record2 = LogRecord(
            ip="127.0.0.2",
            user="user2",
            date="2023-01-02T00:00:00+00:00",
            request="POST /submit HTTP/1.1",
            status=404,
            size=2048,
            referrer="http://example.com",
            agent="Mozilla/5.0"
        )
        self.assertNotEqual(log_record1, log_record2)


if __name__ == '__main__':
    unittest.main()
