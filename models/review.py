from pydantic import BaseModel
from typing import Optional
from datetime import date

class Review(BaseModel):
    review_id: Optional[int]
    user_id: str
    movie_id: int
    platform_id: int
    rating: float
    review_date: date
    headline: Optional[str]
    review_text: Optional[str]
    review_body: Optional[str]
