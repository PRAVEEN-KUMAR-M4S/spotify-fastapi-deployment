
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATA_BASE_URL="postgresql://postgres:praveen@localhost:5432/music_app"
engine=create_engine(DATA_BASE_URL)

SessionLocal=sessionmaker(autoflush=False,bind=engine,autocommit=False)



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
