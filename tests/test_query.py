import unittest
from datetime import datetime, timedelta

from app import app


class TestQuery(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = app.logger
        self.client = app.test_client()
        self.path = '/api'

    def test_notawaiting_equal_1_raise_and_error_entry_to_log(self):
        params = {'notawaiting': '1'}
        url = f"{self.path}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
        request_time = datetime.utcnow()

        with self.assertLogs(self.logger, level='INFO') as logs:
            response = self.client.get(url)

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Process2 closed awaiting.\n')

        # Check first log message
        timestamps = set()
        log = logs.output[0].split(' - ')
        timestamp = datetime.strptime(log[0][-26:], '%Y-%m-%d %H:%M:%S.%f')
        self.assertGreaterEqual(timestamp, request_time)
        self.assertLess(timestamp, request_time + timedelta(milliseconds=10))
        timestamps.add(timestamp)
        self.assertEqual('GET', log[1])
        self.assertEqual(self.path, log[2])
        self.assertEqual(str(params), log[3])

        # Check second log message
        log = logs.output[1].split(' - ')
        timestamp = datetime.strptime(log[0][-26:], '%Y-%m-%d %H:%M:%S.%f')
        timestamps.add(timestamp)
        self.assertEqual('Process1 started.', log[1])

        # Check third log message
        log = logs.output[2].split(' - ')
        timestamp = datetime.strptime(log[0][-26:], '%Y-%m-%d %H:%M:%S.%f')
        timestamps.add(timestamp)
        self.assertEqual('Process2 closed awaiting.', log[1])

        # Compare timestamps
        self.assertEqual(len(timestamps), 1)

    def test_success(self):
        request_time = datetime.utcnow()
        with self.assertLogs(self.logger, level='INFO') as logs:
            response = self.client.get(self.path)

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'OK')

        # Check first log message
        timestamps = set()
        log = logs.output[0].split(' - ')
        timestamp = datetime.strptime(log[0][-26:], '%Y-%m-%d %H:%M:%S.%f')
        self.assertGreaterEqual(timestamp, request_time)
        self.assertLess(timestamp, request_time + timedelta(milliseconds=10))
        timestamps.add(timestamp)
        self.assertEqual('GET', log[1])
        self.assertEqual(self.path, log[2])
        self.assertEqual({}.__str__(), log[3])

        # Check second log message
        log = logs.output[1].split(' - ')
        timestamp = datetime.strptime(log[0][-26:], '%Y-%m-%d %H:%M:%S.%f')
        timestamps.add(timestamp)
        self.assertEqual('Process1 started.', log[1])

        # Check third log message
        log = logs.output[2].split(' - ')
        timestamp = datetime.strptime(log[0][-26:], '%Y-%m-%d %H:%M:%S.%f')
        timestamps.add(timestamp)
        self.assertEqual('Process2 started.', log[1])

        # Check fourth log message
        log = logs.output[3].split(' - ')
        timestamp = datetime.strptime(log[0][-26:], '%Y-%m-%d %H:%M:%S.%f')
        timestamps.add(timestamp)
        self.assertEqual('Process3 started.', log[1])

        # Compare timestamps
        self.assertEqual(len(timestamps), 1)
