from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from contextlib import asynccontextmanager
from src.books.my_routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import reviews_router
from src.tags.routes import tags_router
from src.db.main import myinit__db
from .middleware import register_the_middleware
from src.errors import (
    invalidToken_handler, blockedToken_handler, accessTokenRequired_handler, 
    refreshTokenRequired_handler, userAlreadyExists_handler, insufficientPermission_handler,
    bookNotFound_handler, invalidCredentials_handler, tagNotFound_handler, tagAlreadyExists_handler, 
    userNotFound_handler, userNotVerified_handler, reviewNotFound_handler, tagNotOnBook_handler, tagAlreadyOnBook_handler,
    InvalidToken, BlockedToken, AccessTokenRequired, RefreshTokenRequired, UserAlreadyExists,
    InsufficientPermission, BookNotFound, InvalidCredentials, TagNotFound, TagAlreadyExists, UserNotFound, UserNotVerified, ReviewNotFound, TagNotOnBook, TagAlreadyOnBook
)

@asynccontextmanager
async def mylifespan(app : FastAPI):
    print("Server is starting....")
    await myinit__db()
    print("The Server's code runs from now!")
    yield
    print("Server is shutting down....")
 

version="1.0.0"

app = FastAPI(
    title="The Books API",
    description="This is the REST API for the Books Management web service.",
    version=version,
    docs_url= f"/api/{version}/mydocs",
    redoc_url= f"/api/{version}/myredoc",
    contact= {
        "email": "abdullah.bsse4793@student.iiu.edu.pk"
    }
)


# register_the_middleware(app)


from pathlib import Path
from fastapi.staticfiles import StaticFiles
BASE_DIR = Path(__file__).resolve().parent
# Mount the 'static' folder to the '/static' URL path.
# This handles CSS, JS, images, videos, etc. automatically.
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="my_static"
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags= ["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags= ["Auth"])
app.include_router(reviews_router, prefix=f"/api/{version}/reviews", tags= ["Reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags= ["Tags"])


app.add_exception_handler(InvalidToken, invalidToken_handler)
app.add_exception_handler(BlockedToken, blockedToken_handler)
app.add_exception_handler(AccessTokenRequired, accessTokenRequired_handler)
app.add_exception_handler(RefreshTokenRequired, refreshTokenRequired_handler)
app.add_exception_handler(UserAlreadyExists, userAlreadyExists_handler)
app.add_exception_handler(InsufficientPermission, insufficientPermission_handler)
app.add_exception_handler(BookNotFound, bookNotFound_handler)
app.add_exception_handler(InvalidCredentials, invalidCredentials_handler)
app.add_exception_handler(TagNotFound, tagNotFound_handler)
app.add_exception_handler(TagAlreadyExists, tagAlreadyExists_handler)
app.add_exception_handler(UserNotFound, userNotFound_handler)
app.add_exception_handler(UserNotVerified, userNotVerified_handler)
app.add_exception_handler(ReviewNotFound, reviewNotFound_handler)
app.add_exception_handler(TagNotOnBook, tagNotOnBook_handler)
app.add_exception_handler(TagAlreadyOnBook, tagAlreadyOnBook_handler)


@app.exception_handler(Exception)
async def catch_all_the_errors(request: Request, exc: Exception):
        
    return JSONResponse(
        content={"message": "Oops! Something went wrong on our end."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    


