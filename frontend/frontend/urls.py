from django.contrib import admin
from django.urls import path

from app.views import (
    delete_movie_view,
    home_view,
    login_view,
    movies_view,
    my_reservations_view,
    seats_view,
    showtimes_view,
    book_seat,
    signup_view,
    cancel_reservation_view,
    add_movie,
    admin_movies,
    edit_movie,
    add_showtime
)

urlpatterns = [
    # Django admin (leave this alone)
    path('admin/', admin.site.urls),

    # Auth
    path("", login_view, name="login"),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),

    # User pages
    path("home/", home_view, name="home"),
    path("movies/", movies_view, name="movies"),
    path("showtimes/<int:movie_id>/", showtimes_view, name="showtimes"),
    path("seats/<int:showtime_id>/", seats_view, name="seats"),
    path("book-seat/", book_seat, name="book_seat"),
    path("my-reservations/", my_reservations_view, name="my_reservations"),
    path("cancel-reservation/", cancel_reservation_view, name="cancel_reservation"),

    # 🔥 ADMIN PANEL (your custom one)
    path("dashboard/movies/", admin_movies, name="admin_movies"),
    path("dashboard/add-movie/", add_movie, name="add_movie"),
    path("dashboard/movies/<int:movie_id>/delete/", delete_movie_view, name="delete_movie"),
    path("dashboard/movies/<int:movie_id>/edit/", edit_movie, name="edit_movie"),
    path("dashboard/movies/<int:movie_id>/add-showtime/", add_showtime, name="add_showtime"),
]