import unittest
from app import app


class TestDelete(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_string_return_200_status(self):
        res = self.client.delete('test_string')
        self.assertEqual(res.status_code, 200)

    def test_int_return_200_status(self):
        res = self.client.delete(1)
        self.assertEqual(res.status_code, 200)
