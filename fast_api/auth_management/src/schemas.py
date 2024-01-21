from datetime import datetime
from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, Field

from src.utils.constants import Status
from src.validators import ProviderUrlValidation, RoleIdValidation, UsernameValidation

M = TypeVar('M')

class ClientBase(BaseModel):
    label: str = Field(example='Demo')
    role_id: int = Field(example=1, description='role id')

class DateTimeBase(BaseModel):
    created_at: datetime = Field(readOnly=True, example='2023-04-14 00:13:28.464732')
    updated_at: datetime = Field(readOnly=True, example='2023-04-14 00:13:28.464732')

class DeviceRegistrationBase(BaseModel):
    client_id: int = Field(readOnly=True, example=1, description='client id')
    application_id: int = Field(readOnly=True, example=1, description='application id')
    device_id: str = Field(example='EoitIWOQoE2y', description='device id')
    device_os_version: str = Field(example='12', description='device OS')
    device_platform: str = Field(example='android', description='device platform')
    device_type: str = Field(example='V2025', description='device type')
    reference: str = Field(example='EoitIWOQoE2y', description='random string generated')

class IdBase(BaseModel):
    id: int = Field(readOnly=True, example=1)

class RoleBase(BaseModel):
    username: str = Field(example='safousauth', description='username related to Safous app gateway')
    provider_url: str = Field(example='https://login.auth-dev.ztna.safous.com/v1/auth/local/1/stage/1', description='provider endpoint')

class StatusBase(BaseModel):
    status: Status

class ClientResponse(StatusBase, ClientBase, DateTimeBase, IdBase):
    client_id: str = Field(readOnly=True, example='EoitIWOQoE2y', description='client identifier')

class ClientStore(RoleIdValidation, StatusBase, ClientBase):
    pass

class ClientTokenResponse(DateTimeBase, IdBase):
    expiry_access_token: datetime = Field(readOnly=True, example='2023-04-14 00:13:28.464732')
    expiry_refresh_token: datetime = Field(readOnly=True, example='2023-04-14 00:13:28.464732')
    client_id: int = Field(readOnly=True, example=1, description='relation client.id')

class DeviceRegistrationResponse(StatusBase, DeviceRegistrationBase, DateTimeBase, IdBase):
    pass

class PaginatedResponse(BaseModel, Generic[M]):
    data: list[M] = Field(description='list of items')
    total: int = Field(description='total all')

class RoleResponse(StatusBase, RoleBase, DateTimeBase, IdBase):
    reference_id: int = Field(readOnly=True, example=1, description='reference_id is user id')

class RoleStore(ProviderUrlValidation, UsernameValidation, StatusBase, RoleBase):
    password: str = Field(min_length=6, max_length=128, example='Pa55w0rd', description='password related to Safous app gateway')

class RoleUpdate(ProviderUrlValidation, UsernameValidation, StatusBase, RoleBase):
    password: Annotated[str | None, Field(min_length=6, max_length=128, example='Pa55w0rd', description='password related to Safous app gateway')] = None

class StatusResponse(StatusBase):
    pass

class StatusUpdate(StatusBase):
    pass