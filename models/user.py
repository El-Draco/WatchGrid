from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import date

class User(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    date_of_birth: date
