import unittest
from datetime import datetime, timedelta

from app import app


class TestPath(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = app.logger
        self.client = app.test_client()

    def test_empty_path(self):
        self.path = '/'

    def test_int_path(self):
        self.path = '/1'

    def test_string_path(self):
        self.path = '/string'

    def test_float_path(self):
        self.path = '/1.1'

    def test_many_part_path(self):
        self.path = '/some/long/path'

    def tearDown(self) -> None:
        # Check all invalid combinations
        for params in {'invalid': '1'}, {'invalid': '1', 'test': 'test'}:
            url = f"{self.path}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
            request_time = datetime.utcnow()

            with self.assertLogs(self.logger, level='ERROR') as logs:
                response = self.client.get(url)

            # Check response
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'OK')

            # Check logs
            log = logs.output[0].split(' - ')
            timestamp = datetime.strptime(log[0][-26:], '%Y-%m-%d %H:%M:%S.%f')
            self.assertGreaterEqual(timestamp, request_time)
            self.assertLess(timestamp, request_time + timedelta(milliseconds=10))
            self.assertEqual('GET', log[1])
            self.assertEqual(self.path, log[2])
            self.assertEqual(str(params), log[3])
