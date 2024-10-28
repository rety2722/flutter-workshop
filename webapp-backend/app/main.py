from fastapi import FastAPI

from app.api.main import api_router
from app.core.db import init_db
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)
app.add_event_handler("startup", lambda: init_db())
app.include_router(api_router, prefix=settings.API_V1_STR)
