from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.utils.auth import hash_password, verify_password, create_access_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(email: str, password: str, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(password)
    new_user = User(email=email, password=hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# 🔥 IMPORTANT: expects QUERY PARAMS
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    print("LOGIN ATTEMPT:", email, password)   # 🔥

    user = db.query(User).filter(User.email == email).first()
    print("USER FOUND:", user)   # 🔥

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    print("DB PASSWORD:", user.password)  # 🔥

    if not verify_password(password, user.password):
        print("PASSWORD CHECK FAILED")  # 🔥
        raise HTTPException(status_code=400, detail="Invalid credentials")

    print("LOGIN SUCCESS")  # 🔥

    token = create_access_token(data={"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}