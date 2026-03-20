from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Movie
from app.schemas import MovieCreate, MovieResponse

router = APIRouter()

#  Create movie
@router.post("/movies", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    new_movie = Movie(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


# Get all movies
@router.get("/movies", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()