from pydantic import BaseModel
from typing import Optional
from datetime import date
class Movie(BaseModel):
    movie_id: int
    title: str
    release_date: date  # ISO format 'YYYY-MM-DD'
    duration: Optional[int] = None
    language: str
    image_url: str = None
    avg_rating: float
