
from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.log_config import logger
from app.routes import tarefa1, tarefa2
# from app.config import settings

app = FastAPI(
    title="App Thales",
    default_response_class=ORJSONResponse,
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.logger = logger
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Rotas
app.include_router(tarefa1.router)
app.include_router(tarefa2.router)

@app.get("/", response_class=RedirectResponse, status_code=302, include_in_schema=False)
async def redirect_docs():
    return "/docs"
