from unittest import TestCase
from .client import WeevilsClient, NotLoggedIn
from betamax import Betamax
import os

with Betamax.configure() as config:
    config.cassette_library_dir = os.path.join(os.path.dirname(__file__), 'test_cassettes')

class TestClient(TestCase):

    def _make_client(self):
        return WeevilsClient('gckzkXH1jfttvCdasIksSr8pxHo3M9TMHsXRkmSv', base_url='https://example.com')

    def setUp(self):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    def test_url_building(self):
        client = self._make_client()
        self.assertEqual(client._build_url('just/a/path'), 'https://example.com/just/a/path')
        self.assertEqual(client._build_url('and/some/params', a=1, b='!'), 'https://example.com/and/some/params?a=1&b=%21')

    def test_login_required(self):
        token = 'VM9RQcUS6oKtD0We8cCKtsohGCUnxP'
        refresh = '7dQWaxjHH3h8xoIWzVeCLRjPI8RfPd'
        secret = 'cN1SCXPuj1wKWOMNnxINjE2u7E01YWtnEjSSAo3kmJuWSgyStu204gIA2YL7hX9NikIMyf6kCI8vJGG3QGulThn6R1nGRfH6Kj7qJGN8AfZfHojnNJ8KC9BmyVg7koP0'

        client = self._make_client()
        with Betamax(client._session) as betamax:
            betamax.use_cassette('not-logged-in', record='none')
            with self.assertRaises(NotLoggedIn):
                client.refresh_token(refresh, secret)

        client = self._make_client()
        client.login(token)
        with Betamax(client._session) as betamax:
            betamax.use_cassette('logged-in', record='none')
            client.refresh_token(refresh, secret)
