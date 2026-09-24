import uvicorn
from fastapi import FastAPI

from src.presentation.api import system_router, v1_router
from src.presentation.api.errors import register_exception_handlers


def create_app() -> FastAPI:
    application = FastAPI(title='Library Manager')
    application.include_router(v1_router, prefix='/api')
    application.include_router(system_router)
    register_exception_handlers(application)
    return application


app = create_app()


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
