from fastapi import FastAPI

import app.features.auth.infrastructure.models  # noqa: F401
import app.features.tasks.infrastructure.models  # noqa: F401
from app.core.database import Base, engine
from app.features.auth.presentation.router import router as auth_router
from app.features.tasks.presentation.router import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/documentation",   # Swagger UI
    redoc_url="/redoc",          # or None to turn ReDoc off
    openapi_url="/openapi.json", # schema the UIs need
)
app.include_router(auth_router)
app.include_router(task_router)
