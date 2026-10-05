import logging
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.core.logging_config import setup_logging
from app.db.database import Base, engine, get_db

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.files import router as files_router
from app.routers.admin import router as admin_router


logger = logging.getLogger(__name__)
setup_logging()


def initialize_db() -> None:
    """Create schema when the database is reachable, but do not crash startup if it isn't."""
    for attempt in range(1, 11):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError as exc:
            if attempt == 10:
                logger.warning(
                    "Database unavailable during startup; continuing without schema initialization: %s",
                    exc,
                )
                return
            time.sleep(2)


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_db()
    yield


app = FastAPI(
    title="Secure Backend API",
    description="Secure backend application with JWT, RBAC, file uploads and API security",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(files_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Secure Backend API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/db-test")
def database_test(
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("SELECT 1")
    )

    return {
        "database": "connected",
        "result": result.scalar()
    }