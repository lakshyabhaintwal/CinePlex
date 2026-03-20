from urllib import response

import requests
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        response = requests.post(
            "http://127.0.0.1:8000/login",
            params={"email": email, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]

            request.session["token"] = token
            return redirect("home")
        else:
            return render(request, "login.html", {
                "error": "Invalid email or password"
            })

    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        response = requests.post(
            "http://127.0.0.1:8000/signup",
            params={"email": email, "password": password}
        )

        if response.status_code == 200:
            return redirect("login")
        else:
            return render(request, "signup.html", {
                "error": "User already exists"
            })

    return render(request, "signup.html")

def home_view(request):
    token = request.session.get("token")
    if not token:
        return redirect("login")
    
    response = requests.get(
        "http://127.0.0.1:8000/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    if response.status_code == 200:
        user_email = response.json()
    else:
        user_email = "Error Fetching User"
    
    return render(request, "home.html", {"email":user_email})

def movies_view(request):
    token = request.session.get("token")
    if not token:
        return redirect("login")
    response = requests.get(
        "http://127.0.0.1:8000/movies",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code == 200:
        movies = response.json()
    else:
        movies = []
    return render(request, "movies.html", {"movies": movies})

def showtimes_view(request, movie_id):
    token = request.session.get("token")

    if not token:
        return redirect("login")
    response = requests.get(
        f"http://127.0.0.1:8000/showtimes/{movie_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code == 200:
        showtimes = response.json()
    else:
        showtimes = []
    
    return render(request,"showtimes.html",
                  {"showtimes": showtimes,
                   "movie_id": movie_id
                   })


def seats_view(request, showtime_id):
    token = request.session.get("token")

    if not token:
        return redirect("login")

    response = requests.get(
    "http://127.0.0.1:8000/available-seats",
    params={"showtime_id": showtime_id},
    headers={
        "Authorization": f"Bearer {token}"
    }
)

    data = response.json()
    print("API RESPONSE:", data)

    return render(request, "seats.html", {
        "available_seats": data["available_seats"],
        "booked_seats": data["booked_seats"],
        "showtime_id": showtime_id
    })

def book_seat(request):
    if request.method == "POST":
        token = request.session.get("token")
        seat = request.POST.get("seat")
        showtime_id = request.POST.get("showtime_id")

        response = requests.post(
            "http://127.0.0.1:8000/reserve-seat",
            params={
                "showtime_id": showtime_id,
                "seat_number": seat
            },
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        return redirect(f"/seats/{showtime_id}/")
    
def my_reservations_view(request):
    token = request.session.get("token")

    if not token:
        return redirect("login")

    response = requests.get(
        "http://127.0.0.1:8000/my-reservations",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response.status_code == 200:
        reservations = response.json()
    else:
        reservations = []

    return render(request, "my_reservations.html", {
        "reservations": reservations
    })


def cancel_reservation_view(request):
    if request.method == "POST":
        token = request.session.get("token")
        reservation_id = request.POST.get("reservation_id")

        print("RESERVATION ID:", reservation_id)  # 🔥 debug

        api_response = requests.post(   # 🔥 rename variable
            "http://127.0.0.1:8000/cancel-reservation",
            params={"reservation_id": reservation_id},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        print("CANCEL STATUS:", api_response.status_code)
        print("CANCEL RESPONSE:", api_response.text)

    return redirect("my_reservations")

def add_movie(request):
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "genre": request.POST.get("genre"),
            "poster_url": request.POST.get("poster_url"),
            "duration": int(request.POST.get("duration")),
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/movies",   # ✅ FIXED
                json=data
            )

            if response.status_code in [200, 201]:
                return render(request, "add_movie.html", {
                    "success": "Movie added successfully!"
                })
            else:
                return render(request, "add_movie.html", {
                    "error": response.text
                })

        except Exception:
            return render(request, "add_movie.html", {
                "error": "FastAPI server not running"
            })

    return render(request, "add_movie.html")



def admin_movies(request):
    response = requests.get("http://127.0.0.1:8000/movies")
    movies = response.json()

    return render(request, "admin_movies.html", {"movies": movies})


def delete_movie_view(request, movie_id):
    requests.delete(f"http://127.0.0.1:8000/movies/{movie_id}")
    return redirect("admin_movies")

def edit_movie(request, movie_id):
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "genre": request.POST.get("genre"),
            "poster_url": request.POST.get("poster_url"),
            "duration": int(request.POST.get("duration")),
        }

        requests.put(f"http://127.0.0.1:8000/movies/{movie_id}", json=data)

        return redirect("admin_movies")

    # GET request → fetch movie
    response = requests.get("http://127.0.0.1:8000/movies")
    movies = response.json()

    movie = next((m for m in movies if m["id"] == movie_id), None)

    return render(request, "edit_movie.html", {"movie": movie})

def add_showtime(request, movie_id):
    if request.method == "POST":
        showtime = request.POST.get("showtime")

        requests.post(
            "http://127.0.0.1:8000/showtimes",
            params={
                "movie_id": movie_id,
                "showtime": showtime
            }
        )

        return redirect("admin_movies")

    return render(request, "add_showtime.html", {"movie_id": movie_id})