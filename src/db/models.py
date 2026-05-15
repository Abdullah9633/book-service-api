from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, date


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    username: str
    email: str
    first_name: str
    last_name: str

    is_verified: bool = Field(sa_column=Column(server_default= "false"))

    password_hash: str

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )

    books: list["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    ) 
    reviews: list["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"



class BookTagLink(SQLModel, table=True):
    __tablename__ = "book_tag_links"
    
    book_uid: uuid.UUID = Field(foreign_key="books.uid", primary_key=True)
    tag_uid: uuid.UUID = Field(foreign_key="tags.uid", primary_key=True)



class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    name: str
    writer: str
    price: int
    published_by: str
    published_date: date = Field(sa_column=Column(pg.DATE))
    page_count: int
    language: str

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    user_uid: uuid.UUID | None = Field(default=None, foreign_key="users.uid")

    user: User | None = Relationship(
        back_populates="books", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: list['Review'] | None = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    tags: list["Tag"] = Relationship(
        back_populates="books", sa_relationship_kwargs={"lazy": "selectin"}, link_model= BookTagLink
    )
    
    def __repr__(self):
        return f"<Book {self.name}>"
    
    
    
class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    rating: int = Field(gt=0, le= 5)
    review_text: str

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    # Needs to fix these, bcz review can't exist without a user and book.
    user_uid: uuid.UUID | None = Field(default=None, foreign_key="users.uid")
    book_uid: uuid.UUID | None = Field(default=None, foreign_key="books.uid")

    # Needs to fix these, bcz review can't exist without a user and book.
    user: User | None = Relationship(
        back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )
    book: Book | None = Relationship(
        back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Review for Book {self.book_uid} by User {self.user_uid}>"
    
    
    
class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    name: str
    
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    books: list[Book] = Relationship(
        back_populates="tags", sa_relationship_kwargs={"lazy": "selectin"}, link_model= BookTagLink
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


