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
        
        token = "".join(choices(string.ascii_lowercase, k=10))
        
        return LoginUser(token=token)