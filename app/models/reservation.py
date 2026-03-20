from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    showtime_id = Column(Integer, ForeignKey("showtimes.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    user = relationship("User")
    showtime = relationship("Showtime")