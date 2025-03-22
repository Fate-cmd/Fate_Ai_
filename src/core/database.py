from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
from .logging import logger

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Configure engine with connection pool
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 minutes
    echo=settings.APP_DEBUG
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Prevent expired object issues
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()

# Test database connection
def test_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False 