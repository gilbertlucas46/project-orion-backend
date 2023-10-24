from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.settings.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_TIME_MINUTES
from graphql import GraphQLError
import jwt
from datetime import timedelta, datetime


def generate_token(email):
    # now + token lifespan
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time,
        
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token

def hash_password(pwd):
    ph = PasswordHasher()
    return ph.hash(pwd)

def verify_password(pwd_hash, pwd):
    ph = PasswordHasher()

    try:
        ph.verify(pwd_hash, pwd)
        # from the user instance that we got from the database
        # lets get the password_hash and verify that it is consistent with the "password"
        # that the user provided
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")
