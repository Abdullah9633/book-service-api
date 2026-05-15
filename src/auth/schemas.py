from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from src.books.schemas import Book
from src.reviews.schemas import ReviewModel


class UserCreateModel(BaseModel):
    username: str = Field(max_length= 10)
    email: str = Field(max_length= 50)
    password_hash: str = Field(min_length= 8)
    first_name: str
    last_name: str


class UserLoginModel(BaseModel):
    email: str = Field(max_length= 50)
    password_hash: str = Field(min_length= 8)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_vrified: bool
    created_at: datetime
    updated_at: datetime

    
class UserBooksReviewsModel(UserModel):
    books: list[Book]
    reviews: list[ReviewModel]
    
    
class EmailModel(BaseModel):
    email_addresses: list[str]


class PasswordResetRequestModel(BaseModel):
    email: str
    
    
class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
    
    
