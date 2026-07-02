from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
# For SQLite compatibility during development. Remove connect_args when migrating to PostgreSQL.
if "sqlite" in settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency injector to yield DB sessions per request safely
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()