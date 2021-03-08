import unittest
import datetime
from app import app


class TestNotGetMethods(unittest.TestCase):
    def test_request_make_logs_entry(self) -> None:
        self.client = app.test_client()
        self.url = 'test/url/1/1.2'
        self.params = '?test1=test1&test2=test2'

        for self.method, self.request in [
            ("GET", self.client.get),
            ("DELETE", self.client.delete),
            ("PATCH", self.client.patch),
            ("POST", self.client.post),
            ("PUT", self.client.put),
            ("TRACE", self.client.trace),
        ]:
            now_time = datetime.datetime.utcnow()
            self.request(self.url + self.params)
            with open('main.log') as log:
                last_entry = log.readlines()[-1]
                self.assertIn(self.url, last_entry)
                self.assertIn(self.method, last_entry)
                self.assertIn('test1=test1, test2=test2', last_entry)
                timestamp = datetime.datetime.strptime(last_entry[:26], '%Y-%m-%d %H:%M:%S.%f')
                self.assertGreater(timestamp, now_time)
                self.assertLess(timestamp, now_time + datetime.timedelta(seconds=1))
