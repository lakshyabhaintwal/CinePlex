from fastapi import Depends, FastAPI
from app.database import engine, Base
from app.models import user, movie, showtime, reservation, reserved_seat 
from app.routes import auth_routes,reservation_routes, movie_routes
from app.utils.auth import get_current_user
app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(reservation_routes.router)
app.include_router(movie_routes.router)

@app.get("/")


def root():
    return{"message": "Movie Reservation API is running"}

@app.get("/me")
def read_users_me(current_user: user.User = Depends(get_current_user)):
    return current_user.email