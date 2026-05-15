from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from .utils import decode_token
from src.db.redis import token_in_blocklist

from src.db.main import get_the_session
from .service import UserService
from src.db.models import User
from src.errors import (
    InvalidToken, BlockedToken, RefreshTokenRequired, AccessTokenRequired, InsufficientPermission, UserNotVerified
)
user_service = UserService()



class MyTokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        

    async def __call__(self, request: Request):
        my_creds = await super().__call__(request)

        token = my_creds.credentials
        
        if self.token_valid(token) == False:
            raise InvalidToken()  
        
        token_data = decode_token(token)
        
        if await token_in_blocklist(token_data['jti']):
            raise BlockedToken()
            
        self.check_token_type(token_data)
        return token_data
    
    
    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        
        return token_data is not None
    
    
    def check_token_type(self, token_data: dict) -> None:
        pass



class MyAccessTokenBearer(MyTokenBearer):
    def check_token_type(self, token_data: dict) -> None:
        if token_data['refresh']:
            raise AccessTokenRequired()



class MyRefreshTokenBearer(MyTokenBearer):
    def check_token_type(self, token_data: dict) -> None:
        if not token_data['refresh']:
            raise RefreshTokenRequired()
    


async def get_current_user(
    token_details = Depends(MyAccessTokenBearer()),
    session = Depends(get_the_session)
):
    user_email = token_details['user']['email']
    
    user = await user_service.get_user_by_email(user_email, session)
    
    return user



class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
        
    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.is_verified != True:
            raise UserNotVerified()
        
        if current_user.role in self.allowed_roles:
            return True
        
        raise InsufficientPermission()
        
    
