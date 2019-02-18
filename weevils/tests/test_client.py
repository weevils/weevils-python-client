# -*- coding: utf-8 -*-
from unittest import TestCase
import os
import random
import string

from betamax import Betamax

from ..client import NotLoggedIn, WeevilsClient

with Betamax.configure() as config:
    config.cassette_library_dir = os.path.join(os.path.dirname(__file__), "cassettes")


def _random_key(length):
    charset = string.ascii_letters + string.digits
    return "".join([random.choice(charset) for _ in range(length)])


class TestClient(TestCase):
    def _make_client(self):
        return WeevilsClient(_random_key(16), base_url="https://example.com")

    def setUp(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    def test_url_building(self):
        client = self._make_client()
        self.assertEqual(client._build_url("just/a/path"), "https://example.com/just/a/path")
        # py2 dict sorting non-determenistic so need to test both param possibilities
        results = ("https://example.com/and/some/params?a=1&b=%21", "https://example.com/and/some/params?b=%21&a=1")
        self.assertIn(client._build_url("and/some/params", a=1, b="!"), results)

    def test_login_required(self):
        token = _random_key(16)
        refresh = _random_key(16)
        secret = _random_key(32)

        client = self._make_client()
        with Betamax(client._session) as betamax:
            betamax.use_cassette("not-logged-in", record="none")
            with self.assertRaises(NotLoggedIn):
                client.refresh_token(refresh, secret)

        client = self._make_client()
        client.login(token)
        with Betamax(client._session) as betamax:
            betamax.use_cassette("logged-in", record="none")
            client.refresh_token(refresh, secret)
