from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app.settings.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_TIME_MINUTES
from app.db.models import User
from app.db.database import Session
from graphql import GraphQLError
import jwt
from datetime import timedelta, datetime, timezone

def generate_token(email):
    # now + token lifespan
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time,
        
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token

def get_authenticated_user(context):
    # On every request that our graphql server receives
    # as some context information about that contains
    # the execution context in which that request was made.
    # from there we'll be able to access the request object,
    # the full HTTP request object, and from that request object we'll
    # extract the authorization header.
    request_object = context.get('request')
    auth_header = request_object.headers.get('Authorization')

    token = [None]
    if auth_header:
        token = auth_header.split(" ")

    if auth_header and token[0] == "Bearer" and len(token) == 2:
        try:
            payload = jwt.decode(token[1], SECRET_KEY, algorithms=[ALGORITHM])

            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
                raise GraphQLError("Token has expired")

            session = Session()
            user = session.query(User).filter(User.email == payload.get('sub')).first()

            if not user:
                raise GraphQLError("Could not authenticate user")

            return user
        except jwt.exceptions.PyJWTError:
            raise GraphQLError("Invalid authentication token")
        except Exception:
            raise GraphQLError("Could not authenticate user")
    else:
        raise GraphQLError("Missing authentication token")

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
