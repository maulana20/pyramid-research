import json
import pyotp
import requests
from urllib.parse import urlparse

from src.utils.constants import Endpoint
from src.utils.exceptions import SafousException

class CoreService:
    def __init__(self, url):
        self.session = requests.Session()
        self.url     = url
        self.cookies = {}

    def __get_host(self) -> str:
        parsed_url  = urlparse(self.url)
        origin_host = '.'.join(parsed_url.netloc.split('.')[+1:])
        return f'{parsed_url.scheme}://login.{origin_host}'

    def request(self, method, path, kwargs):
        response = self.session.request(method, f"{self.__get_host()}/{path}", data=kwargs, cookies=self.cookies)
        self.cookies.update(response.cookies.get_dict())
        if 200 <= response.status_code < 300:
            try:
                return json.loads(response.content)
            except:
                return None
        raise SafousException

class SafousService():
    def __init__(self, username, password, url):
        self.client   = CoreService(url)
        self.username = username
        self.password = password
        self.url      = url

    def login(self):
        path = urlparse(self.url).path[+1:]
        return self.client.request('POST', path, {'username': self.username, 'password': self.password})

    def me(self):
        return self.client.request('GET', Endpoint.ME, {})

    def totp_key(self):
        return self.client.request('GET', Endpoint.TOTP_KEY, {})

    def totp_verify(self, mfa_secret):
        totp = pyotp.TOTP(mfa_secret)
        return self.client.request('POST', Endpoint.TOTP_VERIFY, {'code': totp.now(), 'kind': 'totp'})

    def commit(self):
        return self.client.request('POST', Endpoint.COMMIT, {})

    def logout(self):
        return self.client.request('GET', Endpoint.LOGOUT, {})