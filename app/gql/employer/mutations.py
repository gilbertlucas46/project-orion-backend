from graphene import Mutation, String,  Field, Int, Boolean
from app.gql.types import  EmployerObject
from app.db.database import Session
from app.db.models import  Employer, User
from app.settings.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_TIME_MINUTES
from datetime import datetime, timezone
from graphql import GraphQLError
import jwt

# On every request that our graphql server receives
# as some context information about that contains
# the execution context in which that request was made.
# from there we'll be able to access the request object,
# the full HTTP request object, and from that request object we'll
# extract the authorization header.

def get_authenticated_user(context):
    request_object = context.get('request')
    auth_header = request_object.headers.get('Authorization')

    token = [None]
    # check if theres an auth header, split is by space and get second[1] element
    # example
    # "authorization":"Bearer "jwtToken"
    # we want to get the "jwtToken"
    if auth_header:
        token = auth_header.split(" ")

    if auth_header and token[0] == "Bearer" and len(token) == 2:
        try:
            payload = jwt.decode(token[1], SECRET_KEY, algorithms=[ALGORITHM])
            # This will decode JWT and verify that the current time is before the
            # expiration time

            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
                 # if the token is older than the specified time TOKEN_EXPIRATION_TIME_MINUTES
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


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)
        
    employer = Field(lambda: EmployerObject)
    
    authenticated_as = Field(String)
    
    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        user = get_authenticated_user(info.context)
        session = Session()
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session.add(employer)
        session.commit()
        session.refresh(employer)
        # return AddEmployer(employer=employer)
        return AddEmployer(employer=employer, authenticated_as=user.email)

class UpdateEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()
        
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(root, info, employer_id, name=None, contact_email=None, industry=None):
        session = Session()
        employer = session.query(Employer).filter(Employer.id == employer_id).first()

        if not employer:
            raise Exception("employer not found")

        if name is not None:
            employer.name = name
        if contact_email is not None:
            employer.contact_email = contact_email
        if industry is not None:
            employer.industry = industry

        session.add(employer)
        session.commit()
        # we're refreshing the job instance with the current state that it has in the db
        session.refresh(employer)
        return UpdateEmployer(employer=employer)
    

class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    success =  Boolean()
    
    @staticmethod
    def mutate(root, info, id):
        session = Session()
        employer = session.query(Employer).filter(Employer.id == id).first()
        
        if not employer:
            raise Exception("Job not found")
        
        session.delete(employer)
        session.commit()
        session.close()
        return DeleteEmployer(success=True)
