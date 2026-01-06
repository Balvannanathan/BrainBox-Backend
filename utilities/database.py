from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from models import Base


# Create database engine
engine = create_engine(
    f"postgresql://balaaathi:{quote_plus('B@la3321')}@localhost:5432/postgres",
    echo=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database by creating all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
