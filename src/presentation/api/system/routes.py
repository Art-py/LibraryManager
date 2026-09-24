from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=['System'])


@router.get('/healthcheck')
def healthcheck() -> JSONResponse:
    return JSONResponse({'status': 'ok'})
