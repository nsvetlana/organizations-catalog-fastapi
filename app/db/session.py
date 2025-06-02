from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create the SQLAlchemy engine; add special handling for SQLite if needed
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency that can be used with FastAPI's dependency injection system
    to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
