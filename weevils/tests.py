from unittest import TestCase
from .client import WeevilsClient, NotLoggedIn


class TestClient(TestCase):

    def _make_client(self):
        return WeevilsClient('client_id', base_url='https://example.com')

    def test_url_building(self):
        client = self._make_client()
        self.assertEqual(client._build_url('just/a/path'), 'https://example.com/just/a/path')
        self.assertEqual(client._build_url('and/some/params', a=1, b='!'), 'https://example.com/and/some/params?a=1&b=%21')

    def test_login_required(self):
        client = self._make_client()
        with self.assertRaises(NotLoggedIn):
            client.refresh_token('refresh', 'secret')
        client.login('token')
        client.refresh_token('refresh', 'secret')
