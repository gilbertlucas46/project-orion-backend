from graphene import Mutation, String, Int, Field, Boolean
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import User
from argon2.exceptions import VerifyMismatchError
from app.utils.utils import generate_token, verify_password


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
        
        verify_password(user.password_hash, password)
        
        token = generate_token(email)
        
        return LoginUser(token=token)
