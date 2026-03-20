from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal
from app.models.reservation import Reservation
from app.models.reserved_seat import ReservedSeat
from app.models.showtime import Showtime
from app.utils.auth import get_current_user
from app.models.user import User
from app.models.movie import Movie
from app.schemas import MovieCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 Reserve Seat
@router.post("/reserve-seat")
def reserve_seat(
    showtime_id: int,
    seat_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()

    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    seat = db.query(ReservedSeat).filter(
        ReservedSeat.showtime_id == showtime_id,
        ReservedSeat.seat_number == seat_number
    ).first()

    if seat:
        raise HTTPException(status_code=400, detail="Seat already reserved")

    reservation = Reservation(
        user_id=current_user.id,
        showtime_id=showtime_id
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    reserved_seat = ReservedSeat(
        reservation_id=reservation.id,
        showtime_id=showtime_id,
        seat_number=seat_number
    )

    try:
        db.add(reserved_seat)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Seat already reserved")

    return {
        "message": "Seat reserved successfully",
        "seat": seat_number
    }


# 🔹 Available Seats
@router.get("/available-seats")
def get_available_seats(showtime_id: int, db: Session = Depends(get_db)):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()

    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    booked_seats = db.query(ReservedSeat).filter(
        ReservedSeat.showtime_id == showtime_id
    ).all()

    booked = [seat.seat_number for seat in booked_seats]

    all_seats = [
        f"{row}{num}"
        for row in ["A", "B", "C", "D", "E"]
        for num in range(1, 6)
    ]

    available = [seat for seat in all_seats if seat not in booked]

    return {
        "showtime_id": showtime_id,
        "booked_seats": booked,
        "available_seats": available
    }


# 🔹 My Reservations
@router.get("/my-reservations")
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reservations = db.query(Reservation).filter(
        Reservation.user_id == current_user.id
    ).all()

    result = []

    for reservation in reservations:
        showtime = db.query(Showtime).filter(
            Showtime.id == reservation.showtime_id
        ).first()

        movie = db.query(Movie).filter(
            Movie.id == showtime.movie_id
        ).first()

        seats = db.query(ReservedSeat).filter(
            ReservedSeat.reservation_id == reservation.id
        ).all()

        seat_numbers = [seat.seat_number for seat in seats]

        result.append({
            "movie": movie.title,
            "showtime": showtime.showtime,
            "seats": seat_numbers,
            "id": reservation.id
        })

    return result


# 🔹 Cancel Reservation
@router.post("/cancel-reservation")
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.query(ReservedSeat).filter(
        ReservedSeat.reservation_id == reservation_id
    ).delete()

    db.delete(reservation)
    db.commit()

    return {"message": "Reservation cancelled successfully"}


# 🔹 Movies
@router.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()


# 🔹 Showtimes
@router.get("/showtimes/{movie_id}")
def get_showtimes(movie_id: int, db: Session = Depends(get_db)):
    return db.query(Showtime).filter(
        Showtime.movie_id == movie_id
    ).all()

@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if not movie:
        return {"error": "Movie not found"}
    
    db.delete(movie)
    db.commit()
    
    return {"message": "Movie deleted"}

@router.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie_data: MovieCreate, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        return {"error": "Movie not found"}

    for key, value in movie_data.dict().items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)

    return movie

@router.post("/showtimes")
def create_showtime(movie_id: int, showtime: str, db: Session = Depends(get_db)):
    new_showtime = Showtime(
        movie_id=movie_id,
        showtime=showtime
    )

    db.add(new_showtime)
    db.commit()
    db.refresh(new_showtime)

    return new_showtime

