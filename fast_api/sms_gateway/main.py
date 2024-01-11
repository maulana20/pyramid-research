from enum import Enum

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from starlette import status

from dependencies import license_check, public_key_check
from services import CyoloService, YroamingService

app = FastAPI(dependencies=[Depends(license_check), Depends(public_key_check)])

class InternationalNumber(list[str], Enum):
    china= ['+86', '+0086']

class SmsGateway(BaseModel):
    phone_number: str
    redirect_uri: str = Field(min_length=5, max_length=160)
    user_name: str | None = None

@app.post('/v1/sms', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def sms_gateway(request: Request, item: SmsGateway):
    def get_service(phone_number: str):
        for code in InternationalNumber.china:
            if phone_number.startswith(code):
                return YroamingService
        return CyoloService
    get_service(item.phone_number)(request).send(item.dict())

@app.api_route('/{path_name:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def catch_all(request: Request, path_name: str):
    result = CyoloService(request).send(await request.json())
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)