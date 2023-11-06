from graphene import Mutation, String, Int, Field, Boolean
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import User
from argon2.exceptions import VerifyMismatchError
from app.utils.utils import generate_token, verify_password
from app.gql.types import UserObject
from app.utils.utils import hash_password

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
    
class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)
        
    user = Field(lambda: UserObject)
    
    @staticmethod
    def mutate(root, info, username, email, password, role):
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        
        if(user):
            raise GraphQLError("A user with this email already exists.")
        
        password_hash = hash_password(password)
        user = User(username=username, email=email,password_hash=password_hash, role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return AddUser(user=user)
