from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    description: str
    genre: str
    poster_url: str
    duration: int

class MovieResponse(BaseModel):
    id: int
    title: str
    description: str
    genre: str
    poster_url: str
    duration: int

    class Config:
        from_attributes = True   # for SQLAlchemy