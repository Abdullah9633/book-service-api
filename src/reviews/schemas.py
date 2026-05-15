from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(gt= 0, le= 5)
    review_text: str
    created_at: datetime
    updated_at: datetime
    user_uid: uuid.UUID | None
    book_uid: uuid.UUID | None

class ReviewCreateModel(BaseModel):
    rating: int = Field(gt= 0, le= 5)
    review_text: str
    
