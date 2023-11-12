

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Employer, Job, User, JobApplication
from app.db.data import employers_data, jobs_data, users_data, applications_data
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)

# database helper
# drops all the table if any exists
def prepare_database():
    from app.utils.utils import hash_password
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    session = Session()
    
    for employer in employers_data:
        #create a new instance of employer
        emp = Employer(**employer) # "**" destructure/spread the object
        #add it to the session
        session.add(emp)

    for job in jobs_data:
        #create a new instance of employer
        session.add(Job(**job))
        #add it to the session
        
    for user in users_data:
        user["password_hash"] = hash_password(user["password"])
        del user["password"]
        session.add(User(**user))
    
    for app in applications_data:
        session.add(JobApplication(**app))

    session.commit()
    session.close()
