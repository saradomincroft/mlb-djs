from sqlalchemy import Column, String, Integer, Boolean, ForeginKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Dj(Base):
    __tablename__ = "djs"

    id = Column(Integer(), primary_key=True)
    djname = Column(String(), nullable=False)
    genre = Column(String(), nullable=False)
    subgenre = Column(String(), nullable=False)
    produces = Column(Boolean(), nullable=False)
