import unittest
from app import app


class TestNotGetMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_string_return_200_status(self) -> None:
        self.url = 'test_string'

    def test_string_path_return_200_status(self) -> None:
        self.url = 'test/path'

    def test_int_return_200_status(self) -> None:
        self.url = '1'

    def test_int_path_return_200_status(self) -> None:
        self.url = '1/1'

    def test_float_return_200_status(self) -> None:
        self.url = '1.2'

    def test_float_path_return_200_status(self) -> None:
        self.url = '1.2/3.4'

    def test_with_params_return_200_status(self) -> None:
        self.url = 'test/url/1/1.2?test1=test1&test2=test2'

    def tearDown(self) -> None:
        for self.method, self.request in [
            ("GET", self.client.get),
            ("DELETE", self.client.delete),
            ("PATCH", self.client.patch),
            ("POST", self.client.post),
            ("PUT", self.client.put),
            ("TRACE", self.client.trace),
        ]:
            res = self.request(f'{self.url}')
            self.assertEqual(res.status_code, 200)

