from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Showtime(Base):
    __tablename__ = "showtimes"
    id = Column(Integer, primary_key = True, index = True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    showtime = Column(String) 
    price = Column(Integer)
    movie = relationship("Movie")
    