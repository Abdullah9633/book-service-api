# Book API

This is the REST API for the Books Management web service. It provides a robust backend for managing a digital library, featuring secure role-based authentication, book submissions, tagging, user reviews, and background task processing.

## Features

* **Advanced Authentication & Authorization:** Secure endpoints using JWT (JSON Web Tokens) with distinct roles (`admin`, `user`).
* **Comprehensive Book Management:** Full CRUD capabilities for books, including tracking user-specific submissions.
* **Reviews & Tags:** Endpoints designed to attach tags to books and manage user reviews.
* **Asynchronous Database Operations:** Built with `SQLModel`, `SQLAlchemy`, and `asyncpg` for high-performance, non-blocking database queries.
* **Background Task Processing:** Integration with `Celery` and `Redis` for handling delayed operations like sending automated emails (`fastapi-mail`).
* **Automated Migrations:** Database schema management handled smoothly via `Alembic`.
* **Centralized Error Handling:** Standardized, custom exception handlers (e.g., `BookNotFound`, `InvalidToken`, `InsufficientPermission`) for clean API responses.

## Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **ORM/Database:** [SQLModel](https://sqlmodel.tiangolo.com/), SQLAlchemy, PostgreSQL (via `asyncpg`)
* **Caching & Message Broker:** Redis
* **Task Queue:** Celery
* **Authentication:** PyJWT, pwdlib
* **Migrations:** Alembic

## Prerequisites

Ensure you have the following installed on your machine:
* Python 3.13+
* PostgreSQL (or a NeonDB instance)
* Redis Server (running locally on port 6379 or remotely)


## API Documentation

Once the server is running, FastAPI automatically generates interactive API documentation. 
You can access them at:
Swagger UI: [Swagger UI](http://localhost:8000/api/1.0.0/mydocs)
ReDoc: [Redoc](http://localhost:8000/api/1.0.0/myredoc)

## Version
The API is versioned at v1.0.0.
