from models.base import Base
from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship


class Faviroute(Base):
    __tablename__ = "favorite"

    id=Column(Text, primary_key=True)
    song_id=Column(Text, ForeignKey("songs.id"))
    user_id=Column(Text, ForeignKey("users.id"))

    song=relationship("Song")
    user=relationship("User",back_populates="favorite")
