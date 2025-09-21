import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Read the DB URL from environment variables (must be set in Vercel / local .env)
DATABASE_URL = os.environ["DATABASE_URL"]

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Configure session maker
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
