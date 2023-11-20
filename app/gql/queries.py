from graphene import ObjectType, List, Field, Int
from app.gql.types import JobObject, EmployerObject, UserObject, JobApplicationObject, PostObject
from app.db.database import Session
from app.db.models import Job, Employer, User, JobApplication
from app.utils.utils import admin_user, get_authenticated_user


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))
    users = List(UserObject)
    job_applications = List(JobApplicationObject)
    post = Field(PostObject, id=Int(required=True))
    me = Field(UserObject)

    def resolve_job_applications(root, info):
        return Session().query(JobApplication).all()

    @admin_user
    def resolve_users(root, info):
        return Session().query(User).all()

    @staticmethod
    def resolve_job(root, info, id):
        return Session().query(Job).filter(Job.id == id).first()

    @staticmethod
    def resolve_employer(root, info, id):
        return Session().query(Employer).filter(Employer.id == id).first()

    @staticmethod
    def resolve_jobs(root, info):
        return Session().query(Job).all()

    @staticmethod
    def resolve_employers(root, info):
        return Session().query(Employer).all()

    def resolve_me(root, info):
        user = get_authenticated_user(info.context)
        return user
