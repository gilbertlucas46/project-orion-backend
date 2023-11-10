from functools import wraps
from datetime import timedelta, datetime, timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import User
from dotenv import load_dotenv
import os

load_dotenv()
# This invocation will load all of the key value pairs from our .env
# into a massive dictionary "load_dotenv()" that can be access from
#  out OS module
# os.getenv("") this is how we get an environment variable at runtime
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION_TIME_MINUTES = int(os.getenv("TOKEN_EXPIRATION_TIME_MINUTES"))

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


def admin_user(func):
    # Note: 💁 when we wrapped the function with our decorator
    # it looses its original name & docstring which makes problematic
    # including debugging and investigating error messages
    # Its a good practice to copy the to copy the name, docstring as well as the
    # other meta data from the original function to the wrapped function
    # one elegant way to do it is to use functools module "@wraps"
    @wraps(func)
    def wrapper(*args, **kwargs):
        # /single asterisk(positional) double asterisk keyword arguments respectively
        
        # we need to get access to the context
        # which is always second in our mutate function
        info = args[1]
        # get a handle on the authenticated user
        user = get_authenticated_user(info.context)
        print(info.context)
        
        # check whether the user has a role of admin
        if user.role != "admin":
            raise GraphQLError("You are not authorized to perform this action")
        
        # 1.If they are and admin proceed to the rest of the logic
        # 2.Return the invocation of the wrapped function with *args, **kwargs
        # because we dont know in advance what they will be called with
        return func(*args, **kwargs)
        
        # when we return the ❌wrapper() ✅wrapper we do not want to invoke it
        # we simple want to return the wrapped function with the checks
        # that its doing & delegating the invocation of that function
    return wrapper

def authd_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        get_authenticated_user(info.context)
        return func(*args, **kwargs)
        
    return wrapper

def authd_user_same_as(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        info = args[1]
        user = get_authenticated_user(info.context)
        uid = kwargs.get("user_id")

        if user.id != uid:
            raise GraphQLError("You are not authorized to perform this action")
        
        return func(*args, **kwargs)
        
    return wrapper 