from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path # 1. Adicione esta importação

from app.core.config import settings
from app.core.database import engine, Base
from app.routes.ticket import router as ticket_router

from app.models.ticket import Ticket


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="API de Tickets com IA",
    version="0.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket_router)

@app.get("/")
def serve_frontend():
    BASE_DIR = Path(__file__).resolve().parent
    html_path = BASE_DIR / "index.html"
    return FileResponse(html_path)
