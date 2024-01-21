from fastapi import APIRouter, Depends
from fastapi.responses import Response

from src.database import session
from src.dependencies import (
    filter_device_registration_params,
    filter_optional_device_registration_custom_params,
    paginate,
    paginated_params,
    query_filters_set,
    query_optional_device_registration_custom_set,
    valid_device_registration_id)
from src.models import DeviceRegistration
from src.schemas import DeviceRegistrationResponse, PaginatedResponse, StatusResponse, StatusUpdate

router = APIRouter(
    prefix='/api/device/registrations',
    tags=['api device registrations'],
)

@router.get('')
async def list_device_registration_data(
    filters : tuple = Depends(filter_device_registration_params),
    optional: dict = Depends(filter_optional_device_registration_custom_params),
    params  : dict = Depends(paginated_params)) -> PaginatedResponse[DeviceRegistrationResponse]:
    query = session.query(DeviceRegistration)
    query = await query_filters_set(query=query, model=DeviceRegistration, filters=filters)
    query = await query_optional_device_registration_custom_set(query=query, model=DeviceRegistration, optional=optional)
    return await paginate(query=query, model=DeviceRegistration, params=params)

@router.get('/{id}')
async def get_device_registration_data(device_registration: dict = Depends(valid_device_registration_id)) -> DeviceRegistrationResponse:
    return device_registration

@router.delete('/{id}', status_code=204, response_class=Response)
async def delete_device_registration_data(device_registration: dict = Depends(valid_device_registration_id)):
    pass

@router.put('/{id}/status')
async def update_status_device_registration_data(
    data: StatusUpdate,
    device_registration: dict = Depends(valid_device_registration_id)) -> StatusResponse:
    device_registration.status = data.status.value
    session.commit()
    return device_registration