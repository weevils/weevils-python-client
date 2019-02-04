from urllib.parse import urljoin, urlencode
from requests_oauthlib import OAuth2Session
from .models import WeevilUser, Repository


class NotLoggedIn(Exception):
    def __init__(self, method_name):
        return super().__init__("You must log in with a token before using the %s method" % method_name)

def requires_login(meth):
    def ensure_token(instance, *args, **kwargs):
        if getattr(instance, '_token', None) is None:
            raise NotLoggedIn(meth.__name__)
        return meth(instance, *args, **kwargs)
    return ensure_token

class WeevilsClient:

    def __init__(self, client_id, base_url='https://weevils.io'):
        self.client_id = client_id
        self.base_url = base_url

    @property
    def _session(self):
        if hasattr(self, '_token'):
            token = {'access_token': self._token }
        else:
            token = None
        return OAuth2Session(self.client_id, token=token)

    def _build_url(self, path, **params):
        base = urljoin(self.base_url, path)
        if not params:
            return base
        return '%s?%s' % (base, urlencode(params))

    def get_login_github(self, with_state=False):
        auth_url = self._build_url('oauth2/authorize', scope='basic github')
        url, state = self._session.authorization_url(auth_url)
        return (url, state) if with_state else url

    def get_login_bitbucket(self, with_state=False):
        auth_url = self._build_url('oauth2/authorize', scope='basic bitbucket')
        url, state = self._session.authorization_url(auth_url)
        return (url, state) if with_state else url

    def login(self, token):
        self._token = token

    @requires_login
    def refresh_token(self, refresh_token, client_secret):
        token_url = self._build_url('oauth2/token')
        token = self._session.refresh_token(
            token_url,
            refresh_token=refresh_token,
            **{"client_id": self.client_id, "client_secret": client_secret}
        )
        return token

    def get_token(self, from_response, client_secret):
        token_url = self._build_url('oauth2/token')
        return self._session.fetch_token(token_url, authorization_response=from_response, client_secret=client_secret)

    def _auth_get(self, path, **params):
        return self._session.get(self._build_url(path, **params)).json()

    def _auth_post(self, path, query_params=None, **post_data):
        query_params = query_params or {}
        return self._session.post(self._build_url(path, **query_params), data=post_data).json()

    @requires_login
    def user(self):
        return WeevilUser(self._auth_get('api/user'))

    @requires_login
    def list_repositories(self, host=None, owner=None, name=None, checked=None):
        params = {}
        if host is not None:
            params['host'] = host
        if owner is not None:
            params['owner'] = owner
        if name is not None:
            params['name'] = name
        if checked is not None:
            params['checked'] = 'true' if checked else 'false'
        return [
            Repository(data) for data in
            self._auth_get('api/repos/', **params)
        ]

    @requires_login
    def repository_from_id(self, repository_id):
        return Repository(self._auth_get('api/repos/%s' % repository_id))

    @requires_login
    def set_checking(self, repository_id, checking):
        response = self._auth_post('api/repos/%s/checked' % repository_id, enabled=checking)
        return response['enabled']

    def trigger_sync(self):
        pass