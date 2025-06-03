import os
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config

from app.config import settings
from app.db.base import Base
from app.db.session import engine

# Import API routers from our domains.
from app.api.v1.organization_routes import router as organization_router
from app.api.v1.building_routes import router as building_router
from app.api.v1.activity_routes import router as activity_router
from app.api.v1.auth_routes import router as auth_router
from app.auth import get_current_user


def run_migrations():
    """Run pending Alembic migrations on application startup."""
    alembic_cfg = Config("alembic.ini")
    if os.getenv("AUTO_MIGRATE", "true").lower() in ("true", "1", "yes"):
        command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: run migrations (and create tables if needed)
    run_migrations()
    # For development, you might uncomment the following line:
    # Base.metadata.create_all(bind=engine)

    yield  # This yields control to the application while it runs.

    # Shutdown logic (if needed) can be added here.
    # For example: closing database connections or cleaning up resources.


app = FastAPI(
    lifespan=lifespan,
    title="Organization Directory API",
    version="0.1.0",
    description="A REST API for managing organizations, buildings, and activities with JWT authentication using OAuth2 token exchange and Ed25519.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Expose the /auth/token endpoint (public).
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Protect other endpoints using the JWT dependency.
app.include_router(
    organization_router,
    prefix="/organizations",
    tags=["Organizations"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    building_router,
    prefix="/buildings",
    tags=["Buildings"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    activity_router,
    prefix="/activities",
    tags=["Activities"],
    dependencies=[Depends(get_current_user)]
)


@app.get("/")
async def index():
    return {"message": "Welcome to the Organization Directory API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
