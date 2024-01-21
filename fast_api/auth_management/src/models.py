from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
    Text,
    func)
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.utils.constants import Status

Base = declarative_base()

class Application(Base):
    __tablename__ = 'applications'

    id = Column(BigInteger, primary_key=True)
    registration_role_id = Column(BIGINT(unsigned=True), ForeignKey('roles.id'), comment='related role_id for policy to access applications user registration backend')
    transaction_role_id = Column(BIGINT(unsigned=True), ForeignKey('roles.id'), comment='related role_id for policy to access applications backend')
    app_code = Column(String(64), unique=True, index=True, comment='code identifying the applications registered in safous-auth')
    description = Column(String(1024), comment='description of applications')
    public_key = Column(Text, comment='applications public key used for registration token verification process')
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())

    registration_role = relationship('Role', cascade='all,delete', foreign_keys=[registration_role_id])
    transaction_role = relationship('Role', cascade='all,delete', foreign_keys=[transaction_role_id])

class Client(Base):
    __tablename__ = 'clients'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(String(255), unique=True, index=True, comment='client identifier')
    client_secret = Column(String(4096), nullable=False, comment='client secret, encrypted in AES 256 CBC')
    label = Column(String(1024), comment='additional info')
    status = Column(SmallInteger, default=Status.INACTIVE)
    role_id = Column(BIGINT(unsigned=True), ForeignKey('roles.id'), comment='client related to role or policy')
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())

    role = relationship('Role', cascade='all,delete', backref='parent')

class ClientToken(Base):
    __tablename__ = 'client_tokens'

    id = Column(BigInteger, primary_key=True)
    access_token = Column(Text, comment='client access token')
    refresh_token = Column(Text, comment='client refresh token, used to refresh access token')
    expiry_access_token = Column(DateTime, server_default=func.now(), comment='expiry timestamp for access token')
    expiry_refresh_token = Column(DateTime, server_default=func.now(), comment='expiry timestamp for refresh token')
    client_id = Column(BIGINT(unsigned=True), ForeignKey('clients.id'), comment='token record relation to the client record')
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())

    client = relationship('Client', cascade='all,delete', backref='parent')

class DeviceRegistration(Base):
    __tablename__ = 'device_registrations'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(BIGINT(unsigned=True), ForeignKey('clients.id'), comment='device register relation to the created client record')
    application_id = Column(BIGINT(unsigned=True), ForeignKey('applications.id'), unique=True, index=True, comment='device register relation to the apps')
    device_id = Column(String(64), unique=True, index=True, comment='device id from device registration request')
    device_os_version = Column(String(64), comment='device OS from device registration request')
    device_platform = Column(String(64), comment='device platform from device registration request')
    device_type = Column(String(64), comment='device platform from device registration request')
    reference = Column(String(64), comment='device platform from device registration request')
    status = Column(SmallInteger, default=Status.INACTIVE)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())

    client = relationship('Client', cascade='all,delete')
    application = relationship('Application', cascade='all,delete')

class Role(Base):
    __tablename__ = 'roles'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(255), unique=True, index=True, comment='username related to Safous app gateway')
    password = Column(String(255), nullable=False, comment='password related to Safous app gateway, encrypted in AES 256 CBC')
    mfa_key = Column(String(255), comment='MFA seed related to Safous app gateway, encrypted in AES 256 CBC')
    provider_url = Column(String(255), nullable=False, comment='provider endpoint')
    reference_id = Column(BIGINT(unsigned=True), comment='reference_id is user id')
    status = Column(SmallInteger, default=Status.INACTIVE)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())