from enum import Enum

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from starlette import status

from src.routers import clients, device_registrations, roles
from src.utils.exceptions import ValidationException

app = FastAPI()

@app.exception_handler(ValidationException)
async def value_error_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(status_code=422, content={"message": str(exc)})

app.include_router(clients.router)
app.include_router(device_registrations.router)
app.include_router(roles.router)