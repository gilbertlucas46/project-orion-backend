import graphene
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from app.gql.enums import AccountRoleEnum, StatusEnum

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

    applications = relationship(
        "JobApplication", back_populates="job", lazy="joined")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    role = Column(Enum(AccountRoleEnum),
                  default=AccountRoleEnum.USER, nullable=False)
    # use the Enum type directly from SQLAlchemy and set nullable=False instead of
    # nullable=True to ensure that the status column is not nullable since we set a default value
    status = Column(Enum(StatusEnum),
                    default=StatusEnum.PENDING, nullable=False)
    companyName = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    facebookLink = Column(String)
    address = Column(String)
    phoneNumber = Column(String)
    identificationImage = Column(String)
    companyLogoUrl = Column(String)
    applications = relationship(
        "JobApplication", back_populates="user", lazy="joined")
    posts = relationship(
        "Post", back_populates="user", lazy="joined")


class JobApplication(Base):
    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    user = relationship("User", back_populates="applications", lazy="joined")
    job = relationship("Job", back_populates="applications", lazy="joined")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    rating = Column(Float)
    booking_count = Column(Integer)

    user = relationship("User", back_populates="posts", lazy="joined")
    prices = relationship("Price", back_populates="post")
    images = relationship("Image", back_populates="post")
    addons = relationship("Addon", back_populates="post")


class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    vehicle_type = Column(String)
    price = Column(Float)

    post = relationship("Post", back_populates="prices")


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    image_url = Column(String)

    post = relationship("Post", back_populates="images")


class Addon(Base):
    __tablename__ = 'addons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    name = Column(String)
    description = Column(String)
    price = Column(Float)

    post = relationship("Post", back_populates="addons")
