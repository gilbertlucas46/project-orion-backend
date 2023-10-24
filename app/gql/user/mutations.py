import string
from random import choices
from graphene import Mutation, String, Int, Field, Boolean
from graphql import GraphQLError
from app.gql.types import JobObject
from app.db.database import Session
from app.db.models import User
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

import jwt
from datetime import timedelta, datetime

SECRET_KEY = "job_board_app_secret!"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_TIME_MINUTES = 15

def generate_token(email):
    # now + token lifespan
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time,
        
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token

class LoginUser(Mutation):
    class Arguments:
        email = String()
        password = String()
        
    token = String()
    
    @staticmethod
    def mutate(root, info, email, password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        
        if not user:
            raise GraphQLError("a user with that email does no exist")
        
        try:
            ph.verify(user.password_hash, password)
            # from the user instance that we got from the database
            # lets get the password_hash and verify that it is consistent with the "password"
            # that the user provided
        except VerifyMismatchError:
            raise GraphQLError("Invalid password")
        
        token = generate_token(email)
        
        return LoginUser(token=token)