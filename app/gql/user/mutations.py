from graphene import Mutation, String, Int, Field, Boolean
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import JobApplication, User
from argon2.exceptions import VerifyMismatchError
from app.utils.utils import generate_token, verify_password
from app.gql.types import JobApplicationObject, UserObject
from app.utils.utils import hash_password, get_authenticated_user

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
        if role == "admin":
            current_user = get_authenticated_user(info.context)
            if current_user.role != "admin":
                raise GraphQLError('only admin can add new users')
        
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        
        if user:
            raise GraphQLError("A user with this email already exists.")
        
        password_hash = hash_password(password)
        user = User(username=username, email=email,password_hash=password_hash, role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return AddUser(user=user)
    
class ApplyToJob(Mutation):
    class Arguments:
        user_id = Int(required=True)
        job_id = Int(required=True)
        
    # It returns a job application field
    job_application = Field(lambda: JobApplicationObject)
    
    @staticmethod
    def mutate(root, info, user_id, job_id):
        session = Session()
        
        # check first if the job already exist
        existing_application = session.query(JobApplication).filter(
            JobApplication.user_id == user_id,
            JobApplication.job_id == job_id
        ).first()
        
        if existing_application:
            raise GraphQLError("This user has already applied to this job")
        
        # JobApplication -> database model, create new instance
        job_application = JobApplication(user_id=user_id, job_id=job_id)
        session.add(job_application)
        session.commit()
        # Refresh it in order to get the ID that Porsgres assigned
        session.refresh(job_application)
        
        return ApplyToJob(job_application=job_application)
