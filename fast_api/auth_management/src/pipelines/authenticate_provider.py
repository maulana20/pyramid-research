from urllib.parse import parse_qs

from src.services import SafousService
from src.utils.exceptions import SafousException, ValidationException

class AuthenticateProvider:
    def __init__(self, service: SafousService):
        self.service       = service
        self._authenticate = {}

    @property
    def authenticate(self):
        return self._authenticate

    @authenticate.setter
    def authenticate(self, kwargs):
        self._authenticate.update(kwargs)

def login_check(auth_provider: AuthenticateProvider, next):
    try:
        auth_provider.service.login()
    except SafousException:
        raise ValidationException('username or password is wrong')
    return next(auth_provider)

def me_check(auth_provider: AuthenticateProvider, next):
    try:
        result = auth_provider.service.me()
        if result['id']:
            auth_provider.authenticate = {'reference_id': result['id']}
            return next(auth_provider)
    except SafousException:
        pass
    raise ValidationException('cannot get reference_id')

def mfa_secret_check(auth_provider: AuthenticateProvider, next):
    try:
        result = auth_provider.service.totp_key()
        if result['uri']:
            params = parse_qs(result['uri'])
            if params['secret']:
                auth_provider.authenticate = {'mfa_key': params['secret'][0]}
                return next(auth_provider)
    except SafousException:
        pass
    raise ValidationException('cannot get mfa_secret')

def totp_verify_check(auth_provider: AuthenticateProvider, next):
    try:
        auth_provider.service.totp_verify(auth_provider.authenticate.get('mfa_key'))
    except SafousException:
        raise ValidationException('totp verify failed')
    return next(auth_provider)

def commit_check(auth_provider: AuthenticateProvider, next):
    try:
        auth_provider.service.commit()
    except SafousException:
        raise ValidationException('commit failed')
    return next(auth_provider)

def logout_check(auth_provider: AuthenticateProvider, next):
    try:
        auth_provider.service.logout()
    except SafousException:
        raise ValidationException('logout failed')
    return next(auth_provider)