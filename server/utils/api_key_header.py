from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
    APIRouter
)

from fastapi.params import Depends
from fastapi.security import APIKeyHeader

API_TOKEN= "AHGF09JHG12"

router= APIRouter()

api_key_header= APIKeyHeader(name='Token')

@router.get('/protected-route/{token}')
async def protected_route(token: str= Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return {'hello': 'world'}