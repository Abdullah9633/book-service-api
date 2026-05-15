from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class MyApplicationErrors(Exception):
    """This is base class for all custom errors, which i will raise"""
    resolution = "Please provide a valid Access Token"
    
    def __init__(self, detail: str):
        self.detail = detail



class InvalidToken(MyApplicationErrors):
    def __init__(
        self, detail: str = "Your authentication token is invalid or expired."
    ):
        """User has provided an invalid or expired Token"""
        super().__init__(detail=detail)


class BlockedToken(MyApplicationErrors):
    def __init__(self, detail: str = "Your authentication token is blocked."):
        """User has provided a Token, which is revoked (blocked)"""
        super().__init__(detail=detail)


class AccessTokenRequired(MyApplicationErrors):
    def __init__(
        self, detail: str = "Please give Access token, instead of Refresh Token."
    ):
        """User has provided a Refresh Token, when an Access Token is required"""
        super().__init__(detail=detail)


class RefreshTokenRequired(MyApplicationErrors):
    resolution = "Please provide a Refresh Token"
    def __init__(
        self, detail: str = "Please give Refresh token, instead of Access Token."
    ):
        """User has provided a Access Token, when a Refresh Token is required"""
        super().__init__(detail=detail)


class UserAlreadyExists(MyApplicationErrors):
    resolution = "Please use a new Email"
    def __init__(self, detail: str = "This Email is already in use of some user."):
        """User has provided an Email (during Signup), which is already the email of some user"""
        super().__init__(detail=detail)


class InsufficientPermission(MyApplicationErrors):
    resolution = "Don't try to access this functionality"
    def __init__(
        self, detail: str = "You do not have the permission, to perform this action."
    ):
        """User does not have the permission, to perform this action."""
        super().__init__(detail=detail)


class BookNotFound(MyApplicationErrors):
    resolution = "Please try to search for another book"
    def __init__(self, detail: str = "Book is not found."):
        """This book does not exists in the database."""
        super().__init__(detail=detail)


class InvalidCredentials(MyApplicationErrors):
    resolution = "Please write correct Email and Password"
    def __init__(self, detail: str = "Invalid Email or Password."):
        """User entered the invalid email or password, on login"""
        super().__init__(detail=detail)


class TagNotFound(MyApplicationErrors):
    resolution = "Please write name of existing tag"
    def __init__(self, detail: str = "This tag does not exist."):
        """This tag does not exists in the database."""
        """So you cannot delete this."""
        super().__init__(detail=detail)


class TagNotOnBook(MyApplicationErrors):
    resolution = "Please write name of tag, which is existing on book"
    def __init__(self, detail: str = "This tag does not present on book."):
        """This tag does not present on the book."""
        super().__init__(detail=detail)


class TagAlreadyOnBook(MyApplicationErrors):
    resolution = "Please write differnt name for tag"
    def __init__(self, detail: str = "This tag is already present on book."):
        """This tag is already present on book."""
        super().__init__(detail=detail)


class TagAlreadyExists(MyApplicationErrors):
    resolution = "Please write different name for tag"
    def __init__(self, detail: str = "This tag already exists."):
        """This tag already exists."""
        """So you cannot create this tag."""
        super().__init__(detail=detail)


class UserNotFound(MyApplicationErrors):
    resolution = "Please write email of existing user"
    def __init__(self, detail: str = "This user does not exist."):
        """This user does not exists in the database."""
        super().__init__(detail=detail)
        
        
class UserNotVerified(MyApplicationErrors):
    resolution = "Please Check your Email for verification details."
    def __init__(self, detail: str = "This Account is not virified yet."):
        """This user is not verified."""
        super().__init__(detail=detail)
        
        
class ReviewNotFound(MyApplicationErrors):
    resolution = "Please give correct review uid"
    def __init__(self, detail: str = "Review is not found."):
        """This Review does not exists in the database."""
        super().__init__(detail=detail)



# The Function, which will create the Exception Handlers.
def create_exception_handler(statuscode):
    async def exception_handler(request: Request, exc: MyApplicationErrors):

        return JSONResponse(
            content={"message": exc.detail, "resolution": exc.resolution}, status_code=statuscode
        )

    return exception_handler



invalidToken_handler = create_exception_handler(statuscode=status.HTTP_401_UNAUTHORIZED)
blockedToken_handler = create_exception_handler(statuscode=status.HTTP_403_FORBIDDEN)
accessTokenRequired_handler = create_exception_handler(
    statuscode=status.HTTP_401_UNAUTHORIZED
)
refreshTokenRequired_handler = create_exception_handler(
    statuscode=status.HTTP_400_BAD_REQUEST
)
userAlreadyExists_handler = create_exception_handler(
    statuscode=status.HTTP_409_CONFLICT
)
insufficientPermission_handler = create_exception_handler(
    statuscode=status.HTTP_403_FORBIDDEN
)
bookNotFound_handler = create_exception_handler(statuscode=status.HTTP_404_NOT_FOUND)
invalidCredentials_handler = create_exception_handler(
    statuscode=status.HTTP_401_UNAUTHORIZED
)
tagNotFound_handler = create_exception_handler(statuscode=status.HTTP_404_NOT_FOUND)
tagAlreadyExists_handler = create_exception_handler(statuscode=status.HTTP_409_CONFLICT)
userNotFound_handler = create_exception_handler(statuscode=status.HTTP_404_NOT_FOUND)
userNotVerified_handler = create_exception_handler(statuscode=status.HTTP_401_UNAUTHORIZED)
reviewNotFound_handler = create_exception_handler(statuscode=status.HTTP_404_NOT_FOUND)
tagNotOnBook_handler = create_exception_handler(statuscode=status.HTTP_404_NOT_FOUND)
tagAlreadyOnBook_handler = create_exception_handler(statuscode=status.HTTP_409_CONFLICT)

