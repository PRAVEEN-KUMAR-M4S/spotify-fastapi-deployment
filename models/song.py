from models.base import Base

from sqlalchemy import TEXT, VARCHAR, Column


class Song(Base):
    __tablename__ = "songs"

    id = Column(TEXT, primary_key=True)
    artist = Column(TEXT)
    song_name = Column(VARCHAR(100))
    hex_code = Column(VARCHAR(6))
    song_url = Column(TEXT)
    thumbnail_url = Column(TEXT)
