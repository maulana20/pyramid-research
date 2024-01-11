import jwt
import time

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()

async def license_check(token: str = Depends(token_auth_scheme)):
    if not token.credentials:
        raise HTTPException(status_code=403, detail="Unauthorized")

async def public_key_check(token: str = Depends(token_auth_scheme)):
    decode = None
    try:
        decode = jwt.decode(token.credentials, open("public.pem").read(), algorithms=["RS256"])
    except jwt.exceptions.InvalidSignatureError:
        pass
    if not decode:
        raise HTTPException(status_code=403, detail="Failed verify")
    if decode.get("validation_end") < time.time():
        raise HTTPException(status_code=403, detail="Token expired")
    if "sms" not in decode.get("features"):
        raise HTTPException(status_code=403, detail="Feature sms not found")