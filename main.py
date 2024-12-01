from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import user_router, content_router
from db import engine, Base

Base.metadata.create_all(engine)
app = FastAPI(
    title='tutorial-server'
)
origins = [
    "http://localhost:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

api = APIRouter(prefix='/api')
api.include_router(user_router)
api.include_router(content_router)
app.include_router(api)

app.mount('/', StaticFiles(directory='frontend', html=True), name='front')
