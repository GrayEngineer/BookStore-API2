#this has the schema of db tables and is use/neede when we have to update data in a table.
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    published_date: datetime
    created_at: datetime
    updated_at: datetime
    #user_id: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    published_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: Optional[int] = None
