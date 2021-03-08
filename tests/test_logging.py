import unittest
from datetime import datetime, timedelta

from app import app


class TestLogging(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()
        self.path = 'test/url/1/1.2'
        self.params = 'first_param=first_value&second_param=second_value'
        self.url = f'{self.path}?{self.params}'

    def test_request_make_logs_entries(self) -> None:
        for self.method, self.request, self.level in [
            ("GET", self.client.get, 'INFO'),
            ("DELETE", self.client.delete, 'ERROR'),
            ("PATCH", self.client.patch, 'ERROR'),
            ("POST", self.client.post, 'ERROR'),
            ("PUT", self.client.put, 'ERROR'),
            ("TRACE", self.client.trace, 'ERROR'),
        ]:

            now_time = datetime.utcnow()
            now_time = now_time - timedelta(microseconds=now_time.microsecond)

            self.request(self.url)

            with open('main.log') as log:
                last_entry = log.readlines()[-1]
                self.assertIn(self.path, last_entry)
                self.assertIn(self.method, last_entry)
                self.assertIn(self.level, last_entry)
                self.assertIn("{'first_param': 'first_value', 'second_param': 'second_value'}", last_entry)

                timestamp = datetime.strptime(last_entry[:19], '%Y-%m-%d %H:%M:%S')
                self.assertGreaterEqual(timestamp, now_time)
                self.assertLess(timestamp, now_time + timedelta(seconds=1))
