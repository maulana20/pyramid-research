from urllib.parse import urlparse

from fastapi import Request
from pydantic import BaseModel, model_validator

from src.database import session
from src.models import Role
from src.utils.exceptions import ValidationException

class ProviderUrlValidation(BaseModel):
    @model_validator(mode='before')
    def provider_url_must_be_valid(cls, values):
        parsed_url = urlparse(values.get('provider_url'))
        if not (parsed_url.scheme and parsed_url.netloc):
            raise ValidationException('provider_url is not valid')
        return values

class RoleIdValidation(BaseModel):
    @model_validator(mode='before')
    def role_id_must_be_valid(cls, values):
        role = session.query(Role).get(values.get('role_id'))
        if role:
            return values
        raise ValidationException('role_id is not valid')

class UsernameValidation(BaseModel):
    @model_validator(mode='before')
    def username_must_be_unique(cls, values):
        role = session.query(Role).filter_by(username=values.get('username')).first()
        if role:
            raise ValidationException('username is already in used')
        return values