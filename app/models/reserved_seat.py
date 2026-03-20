from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint 
from sqlalchemy.orm import relationship
from app.database import Base   
from app.models.reservation import Reservation

class ReservedSeat(Base):
    __tablename__ = "reserved_seats"
    id = Column(Integer, primary_key = True, index = True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    showtime_id = Column(Integer, ForeignKey("showtimes.id"))
    seat_number = Column(String)
    reservation = relationship(Reservation)

    __table_args = (
        UniqueConstraint("showtime_id", "seat_number", name="unique_seat_per_showtime"),
    )