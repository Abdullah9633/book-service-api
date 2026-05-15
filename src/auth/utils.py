from pwdlib import PasswordHash
import jwt
import uuid
from datetime import datetime, timedelta
from src.config import my_config
import logging
from itsdangerous import URLSafeTimedSerializer


# This automatically configures pwdlib, to use the highly secure Argon2 algorithm
my_password_hash = PasswordHash.recommended()

def generate_password_hash(password: str) -> str:
    my_hash = my_password_hash.hash(password)
    return my_hash

def verify_password(password: str, hash: str) -> bool:
    check = my_password_hash.verify(password, hash)

    return check


Expiry_time = 3600

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=Expiry_time)
        )
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload= payload,
        key= my_config.My_JWT_secret,
        algorithm= my_config.My_JWT_algorithm
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
        jwt= token,
        key= my_config.My_JWT_secret,
        algorithms= [my_config.My_JWT_algorithm]
        )

        return token_data
    
    except jwt.exceptions.InvalidTokenError as e:
        logging.exception(e)
        return None


the_serializer = URLSafeTimedSerializer(
    secret_key= my_config.My_JWT_secret,
)

def create_the_url_safe_token(data: dict):
    the_token = the_serializer.dumps(data, salt= "Coconut is sweet")
    return the_token

def decode_the_url_safe_token(token: str):
    try:
        the_data = the_serializer.loads(token, salt= "Coconut is sweet", max_age=3600)
        return the_data
    except Exception as e:
        logging.error(str(e))
        return {"error": "Token is invalid or expired"}


