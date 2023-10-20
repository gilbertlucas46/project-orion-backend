from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

# lazy="joined" it specifies SQLAlchemy that we want to load the relational attributes
# meaning do not lazily evaluate the do not wait.

class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    # autoincrement=True so everytime a db insert happens the id auto increment without us needing to specify
    name = Column(String)
    contact_email = Column(String)
    industry = Column(String) 
    jobs = relationship("Job", back_populates="employer", lazy="joined")


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs", lazy="joined")