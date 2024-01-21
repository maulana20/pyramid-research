from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from sqlalchemy import update

from src.database import session
from src.dependencies import (
    filter_client_params,
    filter_optional_params,
    paginate,
    paginated_params,
    query_filters_set,
    query_optional_set,
    valid_client_id)
from src.models import Client, ClientToken
from src.schemas import ClientResponse, ClientStore, ClientTokenResponse, PaginatedResponse, StatusResponse, StatusUpdate

router = APIRouter(
    prefix='/api/clients',
    tags=['api clients'],
    responses={404: {'description': 'Not found'}},
)

@router.get('')
async def list_client_data(
    filters : tuple = Depends(filter_client_params),
    optional: dict = Depends(filter_optional_params),
    params  : dict = Depends(paginated_params)) -> PaginatedResponse[ClientResponse]:
    query = session.query(Client)
    query = await query_filters_set(query=query, model=Client, filters=filters)
    query = await query_optional_set(query=query, model=Client, optional=optional)
    return await paginate(query=query, model=Client, params=params)

@router.get('/{id}')
async def get_client_data(client: dict = Depends(valid_client_id)) -> ClientResponse:
    return client

@router.put('/{id}')
async def update_client_data(
    data  : ClientStore,
    client: dict = Depends(valid_client_id)) -> ClientResponse:
    session.execute(update(Client).where(Client.id == client.id).values(jsonable_encoder(data)))
    return client

@router.delete('/{id}', status_code=204, response_class=Response)
async def delete_client_data(client: dict = Depends(valid_client_id)):
    pass

@router.put('/{id}/status')
async def update_status_client_data(
    data  : StatusUpdate,
    client: dict = Depends(valid_client_id)) -> StatusResponse:
    client.status = data.status.value
    session.commit()
    return client

@router.get('/{id}/sessions')
async def list_client_sessions_data(client: dict = Depends(valid_client_id)) -> list[ClientTokenResponse]:
    return session.query(ClientToken).filter_by(client_id=client.id).all()