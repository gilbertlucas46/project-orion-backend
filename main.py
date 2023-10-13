from graphene import Schema, ObjectType, String , Int, Field, List, Mutation
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
from sqlalchemy import create_engine, Column, Integer, String as SQLstring, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DB_URL = "postgresql://postgres:yTVwE9Nq4XoDyShnEPgZ@containers-us-west-174.railway.app:7345/railway"
engine = create_engine(DB_URL)

Base = declarative_base()

class Employer(Base):
    __tablename__ = "employers"
    
    id = Column(Integer, primary_key=True)
    name = Column(SQLstring)
    contact_email = Column(SQLstring)
    industry = Column(SQLstring)
    jobs = relationship("Job", back_populates="employer")
    
class Jobs(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    title = Column(SQLstring)
    description = Column(SQLstring)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")

Base.metadata.create_all(engine)

employers_data = [
    {"id": 1, "name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"id": 2, "name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"id": 1, "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"id": 2, "title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"id": 3, "title": "Accountant", "description": "Manage financial records", "employer_id": 2},
    {"id": 4, "title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]

# 💁 lambda the actual evaluation of the type is postponed until it is needed, allowing both 
# classes to be defined without running in to issues related to circular dependencies

class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject) # "lambda" defer undefined class names
    
    @staticmethod
    def resolve_jobs(root, infor):
        return [job for job in jobs_data if job["employer_id"] == root["id"]]
class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda:EmployerObject) # a job is associated with a single employer
    # The next() function is used to retrieve the next item from
    # the iterable created by the generator expression. In this case, it will
    # return the first employer that matches the condition.
    @staticmethod
    def resolve_employer(root, info):
        return next((employer for employer in employers_data if employer["id"] == root["employer_id"]), None)

class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)
    
    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data
    
    @staticmethod
    def resolve_employers(root, info):
        return employers_data
    
schema = Schema(query=Query)

app = FastAPI()

# mount on graphql API
app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))
# at this point we are exposing our graphql API at "/graphql" endpoint of out web application