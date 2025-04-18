from typing import Optional

from pydantic import BaseModel, HttpUrl

class Platform(BaseModel):
    platform_id: int
    name: str
    url: Optional[HttpUrl]
