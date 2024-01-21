from enum import Enum

class Endpoint:
    COMMIT      = 'v1/users/me/commit'
    LOGOUT      = 'cyolo/v1/logout'
    ME          = 'v1/users/me'
    TOTP_KEY    = 'v1/users/me/totp-key-uri'
    TOTP_VERIFY = 'v1/users/me/verify'

class Status(int, Enum):
    INACTIVE = 0
    ACTIVE   = 1