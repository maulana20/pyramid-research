from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from sqlalchemy import insert, update
from sqlalchemy.sql import literal_column

from src.database import session
from src.dependencies import authenticate_provider_check, valid_role_id
from src.models import Role
from src.schemas import RoleResponse, RoleStore, RoleUpdate, StatusResponse, StatusUpdate

router = APIRouter(
    prefix='/api/roles',
    tags=['api roles'],
)

@router.get('')
async def list_role_data() -> list[RoleResponse]:
    return session.query(Role).all()

@router.post('')
async def create_role_data(
    request: Request,
    data   : RoleStore) -> RoleResponse:
    authenticate = await authenticate_provider_check(request)
    role = session.execute(insert(Role).values({**jsonable_encoder(data), **authenticate}).returning(literal_column('*')))
    return role.first()

@router.get('/{id}')
async def get_role_data(role: dict = Depends(valid_role_id)) -> RoleResponse:
    return role

@router.put('/{id}')
async def update_role_data(
    request: Request,
    data   : RoleUpdate,
    role   : dict = Depends(valid_role_id)) -> RoleResponse:
    await authenticate_provider_check(request)
    session.execute(update(Role).where(Role.id == role.id).values(jsonable_encoder(data, exclude_unset=True)))
    return role

@router.delete('/{id}', status_code=204, response_class=Response)
async def delete_role_data(role: dict = Depends(valid_role_id)):
    pass

@router.put('/{id}/status')
async def update_status_role_data(
    data: StatusUpdate,
    role: dict = Depends(valid_role_id)) -> StatusResponse:
    role.status = data.status.value
    session.commit()
    return role