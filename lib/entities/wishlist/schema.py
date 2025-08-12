from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class WishlistResponseSchema(BaseModel):
    id: int
    user_id: int
    book_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
