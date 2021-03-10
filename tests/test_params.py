import unittest
from datetime import datetime, timedelta

from app import app

TESTED_PATHS = [
    '/api',
    '/',
    '/1',
    '/string',
    '/1.1',
    '/some/long/path'
]


class TestInvalid(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = app.logger
        self.client = app.test_client()

    def test_invalid_is_1(self):
        self.params = {'invalid': '1'}

    def test_invalid_is_1_plus_other_param(self):
        self.params = {'invalid': '1', 'test': 'test'}

    def tearDown(self) -> None:
        # Check all invalid combinations
        for path in TESTED_PATHS:
            url = f"{path}?{'&'.join(f'{key}={value}' for key, value in self.params.items())}"
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
            self.assertEqual(path, log[2])
            self.assertEqual(str(self.params), log[3])
