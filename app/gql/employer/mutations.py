from graphene import Mutation, String,  Field, Int, Boolean
from app.gql.types import  EmployerObject
from app.db.database import Session
from app.db.models import  Employer
from app.utils.utils import admin_user

class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)
        
    employer = Field(lambda: EmployerObject)
    
    authenticated_as = Field(String)
    
    @admin_user
    def mutate(root, info, name, contact_email, industry):
        session = Session()
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session.add(employer)
        session.commit()
        session.refresh(employer)

        return AddEmployer(employer=employer)

class UpdateEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()
        
    employer = Field(lambda: EmployerObject)

    @admin_user
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
    
    @admin_user
    def mutate(root, info, id):
        session = Session()
        employer = session.query(Employer).filter(Employer.id == id).first()
        
        if not employer:
            raise Exception("Job not found")
        
        session.delete(employer)
        session.commit()
        session.close()
        return DeleteEmployer(success=True)
