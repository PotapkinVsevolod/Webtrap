import unittest
from datetime import datetime, timedelta

from app import app


TESTED_PARAMS = [
    {},
    {'test': 'test'},
    {'invalid': '1'},
    {'invalid': '1', 'test': 'test'},
    {'invalid': 'test'},
    {'invalid': 'test', 'test': 'test'}
]

TESTED_PATHS = [
    '/api',
    '/',
    '/1',
    '/string',
    '/1.1',
    '/some/long/path'
]


class TestMethod(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = app.logger
        self.client = app.test_client()

    def test_delete(self):
        self.method = "DELETE"
        self.request = self.client.delete

    def test_patch(self):
        self.method = "PATCH"
        self.request = self.client.patch

    def test_post(self):
        self.method = "POST"
        self.request = self.client.post

    def test_put(self):
        self.method = "PUT"
        self.request = self.client.put

    def test_trace(self):
        self.method = "TRACE"
        self.request = self.client.trace

    def tearDown(self) -> None:
        # Check all invalid combinations
        for path in TESTED_PATHS:
            for params in TESTED_PARAMS:
                url = f"{path}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
                request_time = datetime.utcnow()

                with self.assertLogs(self.logger, level='ERROR') as logs:
                    response = self.request(url)

                # Check response
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, b'OK')

                # Check logs
                log = logs.output[0].split(' - ')
                timestamp = datetime.strptime(log[0][-26:], '%Y-%m-%d %H:%M:%S.%f')
                self.assertGreaterEqual(timestamp, request_time)
                self.assertLess(timestamp, request_time + timedelta(milliseconds=10))
                self.assertEqual(self.method, log[1])
                self.assertEqual(path, log[2])
                self.assertEqual(str(params), log[3])

