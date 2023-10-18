

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Employer, Job
from app.settings.config import DB_URL
from app.db.data import employers_data, jobs_data
 
# engine = create_engine(DB_URL)
 
engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)

# database helper
# drops all the table if any exists
def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    session = Session()
    
    for employer in employers_data:
        #create a new instance of employer
        emp = Employer(**employer) # "**" destructure the object
        #add it to the session
        session.add(emp)

    for job in jobs_data:
        #create a new instance of employer
        session.add(Job(**job))
        #add it to the session

    session.commit()
    session.close()
