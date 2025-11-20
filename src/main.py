import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.adapters.api import routers_v1

app = FastAPI(
    title='Library Manager',
)

app.include_router(routers_v1, prefix='/api')


@app.get(path='/healthcheck', tags=['System'])
def healthcheck():
    return JSONResponse({'status': 'ok'})


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
