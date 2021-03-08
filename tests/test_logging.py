import unittest
from datetime import datetime, timedelta

from app import app


class TestNotGetMethods(unittest.TestCase):
    def test_request_make_logs_entry(self) -> None:
        self.client = app.test_client()
        self.path = 'test/url/1/1.2'
        self.params = 'first_param=first_value&second_param=second_value'
        self.url = f'{self.path}?{self.params}'

        for self.method, self.request in [
            ("GET", self.client.get),
            ("DELETE", self.client.delete),
            ("PATCH", self.client.patch),
            ("POST", self.client.post),
            ("PUT", self.client.put),
            ("TRACE", self.client.trace),
        ]:

            now_time = datetime.utcnow()
            now_time = now_time - timedelta(microseconds=now_time.microsecond)

            self.request(self.url)

            with open('main.log') as log:
                last_entry = log.readlines()[-1]
                self.assertIn(self.path, last_entry)
                self.assertIn(self.method, last_entry)
                self.assertIn("{'first_param': 'first_value', 'second_param': 'second_value'}", last_entry)

                timestamp = datetime.strptime(last_entry[:19], '%Y-%m-%d %H:%M:%S')
                self.assertGreaterEqual(timestamp, now_time)
                self.assertLess(timestamp, now_time + timedelta(seconds=1))
