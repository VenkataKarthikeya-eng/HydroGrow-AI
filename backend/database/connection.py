import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.database.database_config import DATABASE_URL

# Detect if we are currently running inside a unit test execution
is_testing = (
    os.getenv("TESTING", "false").lower() == "true" or
    "unittest" in sys.modules or
    any("unittest" in arg for arg in sys.argv)
)

if is_testing:
    # Use a file-based temporary SQLite database for unit tests to allow session sharing across endpoints
    DB_URL = "sqlite:///./test_hydrogrow.db"
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
else:
    DB_URL = DATABASE_URL
    engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
