from graphene import Mutation, String,  Field
from app.gql.types import  EmployerObject
from app.db.database import Session
from app.db.models import  Employer

class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)
        
    employer = Field(lambda: EmployerObject)
    
    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        session = Session()
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session.add(employer)
        session.commit()
        session.refresh(employer)
        return AddEmployer(employer=employer)
    