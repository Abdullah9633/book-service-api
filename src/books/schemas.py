from pydantic import BaseModel
import uuid
from datetime import datetime, date
from src.reviews.schemas import ReviewModel
    
    
class Book(BaseModel):
    uid: uuid.UUID
    name: str
    writer: str
    price: int
    published_by: str
    published_date: date # Bcz it is model, to send back a response to user. As We are sending a database row, in response to user. In database, it is date. So in response, it must be also a date.
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime
    
    
class BookDetailModel(Book):
    reviews: list[ReviewModel]


# Book Create Model
class BookCreateModel(BaseModel):
    name: str
    writer: str
    price: int
    published_by: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    price: int
    published_by: str
    published_date: str
    page_count: int
    updated_at: datetime = datetime.now()


