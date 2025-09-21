
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os   


DATA_BASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_ELjDoX5qF3Yx@ep-calm-leaf-ad9rqheu-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
)
engine=create_engine(DATA_BASE_URL)

SessionLocal=sessionmaker(autoflush=False,bind=engine,autocommit=False)



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
