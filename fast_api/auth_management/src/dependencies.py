from datetime import datetime

from fastapi import Depends, HTTPException, Path, Request, Query
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy import asc, and_, desc

from src.database import session
from src.models import Client, DeviceRegistration, Role
from src.pipelines.authenticate_provider import (
    AuthenticateProvider,
    login_check,
    me_check,
    mfa_secret_check,
    totp_verify_check,
    commit_check,
    logout_check)
from src.pipelines.pipeline import Pipeline
from src.services import SafousService

### parameter

async def filter_client_params(
    client_id: Annotated[str | None, Query(example='EoitIWOQoE2y', description='client identifier')] = None,
    label    : Annotated[str | None, Query(example='12', description='label')] = None) -> tuple:
    return (
        ('client_id', client_id),
        ('label', label)
    )

async def filter_device_registration_params(
    device_id        : Annotated[str | None, Query(example='EoitIWOQoE2y', description='device id')] = None,
    device_os_version: Annotated[str | None, Query(example='12', description='device OS')] = None,
    device_platform  : Annotated[str | None, Query(example='android', description='device platform')] = None,
    device_type      : Annotated[str | None, Query(example='V2025', description='device type')] = None) -> tuple:
    return (
        ('device_id', device_id),
        ('device_os_version', device_os_version),
        ('device_platform', device_platform),
        ('device_type', device_type)
    )

async def filter_optional_params(
    start_datetime: Annotated[datetime | None, Query(example='2023-04-14 00:13:28.464732', description='parameter is "timestamp" with "range"')] = None,
    end_datetime  : Annotated[datetime | None, Query(example='2023-04-14 00:13:28.464732', description='parameter is "timestamp" with "range"')] = None) -> dict:
    return {
        'start_datetime': start_datetime,
        'end_datetime'  : end_datetime
    }

async def filter_optional_device_registration_custom_params(
    optional : dict = Depends(filter_optional_params),
    client_id: Annotated[int | None, Query(example=1, description='relation client.id')] = None) -> dict:
    optional.update({
        'client_id': client_id
    })
    return optional

async def paginated_params(
    page    : int = Query(default=1, description='Number of data to get per page'),
    per_page: int = Query(default=10, le=100, description='Number of page'),
    sort    : str = Query(default='-id', description='Sort key (+: desc, -: asc)')) -> dict:
    return {
        'page'    : page,
        'per_page': per_page,
        'sort'    : sort
    }

async def valid_client_id(id: Annotated[int, Path(example=1, description='ID')]) -> dict:
    result = session.query(Client).get(id)
    if not result:
        raise HTTPException(status_code=404, detail="ID not found")
    return result

async def valid_device_registration_id(id: Annotated[int, Path(example=1, description='ID')]) -> dict:
    result = session.query(DeviceRegistration).get(id)
    if not result:
        raise HTTPException(status_code=404, detail="ID not found")
    return result

async def valid_role_id(id: Annotated[int, Path(example=1, description='ID')]) -> dict:
    result = session.query(Role).get(id)
    if not result:
        raise HTTPException(status_code=404, detail="ID not found")
    return result

### function

async def authenticate_provider_check(request: Request) -> dict:
    params = await request.json()
    if request.method == 'POST':
        password = params['password']
    else:
        role = session.query(Role).get(request.path_params.get('role_id'))
        password = params['password'] if 'password' in params and params['password'] else role.password
    auth_provider = AuthenticateProvider(SafousService(
        params['username'],
        password,
        params['provider_url']))

    result = Pipeline(auth_provider).through([
        login_check,
        me_check,
        mfa_secret_check,
        totp_verify_check,
        commit_check,
        logout_check
    ] if request.method == 'POST' else [
        login_check,
        logout_check
    ]).run()
    return result.authenticate

async def paginate(query: session.query, model: BaseModel, params: dict) -> dict:
    page  = params['page'] * params['per_page'] - params['per_page']
    order = desc if params['sort'][:+1] == '-' else asc
    return {
        'data' : query.order_by(order(getattr(model, params['sort'][+1:])))
            .offset(page)
            .limit(params['per_page'])
            .all(),
        'total': query.count()
    }

async def query_filters_set(query: session.query, model: BaseModel, filters: tuple | None = None) -> session.query:
    if filters is not None:
        expr  = [getattr(model, attr).contains(value) for attr, value in filters if value is not None]
        query = query.filter(and_(*expr))
    return query

async def query_optional_set(query: session.query, model: BaseModel, optional: dict | None = None) -> session.query:
    if optional is not None:
        if optional['start_datetime'] is not None:
            query = query.where(model.created_at >= optional['start_datetime'])
        if optional['end_datetime'] is not None:
            query = query.where(model.created_at <= optional['end_datetime'])
    return query

async def query_optional_device_registration_custom_set(query: session.query, model: BaseModel, optional: dict | None = None) -> session.query:
    query = await query_optional_set(query=query, model=model, optional=optional)
    if optional['client_id'] is not None:
        query = query.where(model.client_id==optional['client_id'])
    return query