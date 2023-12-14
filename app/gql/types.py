from graphene import ObjectType, String, Int, List, Field, Float, Enum, Union
from app.db.models import User
from app.gql.enums import AccountRoleGQLEnum, StatusGQLEnum
import sqlalchemy


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)  # "lambda" defer undefined class names

    @staticmethod
    def resolve_jobs(root, info):
        return root.jobs


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    # a job is associated with a single employer
    employer = Field(lambda: EmployerObject)
    # The next() function is used to retrieve the next item from
    # the iterable created by the generator expression. In this case, it will
    # return the first employer that matches the condition.
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_applications(root, info):
        return root.applications

    @staticmethod
    def resolve_employer(root, info):
        return root.employer


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = Field(AccountRoleGQLEnum)
    status = Field(StatusGQLEnum)
    companyName = String()
    firstName = String()
    lastName = String()
    facebookLink = String()
    address = String()
    phoneNumber = String()
    identificationImage = String()
    companyLogoUrl = String()
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_applications(root, info):
        return root.applications


class AuthenticatedItemUnion(Union):
    class Meta:
        types = (UserObject,)

    @staticmethod
    def resolve_type(instance, info):
        if isinstance(instance, User):
            return UserObject
        # Add other types as needed

        raise Exception('Unknown type')


class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field(lambda: UserObject)
    job = Field(lambda: JobObject)

    @staticmethod
    def resolve_user(root, info):
        return root.user

    @staticmethod
    def resolve_job(root, info):
        return root.job


class PriceObject(ObjectType):
    vehicle_type = String()
    price = Float()


class ImageObject(ObjectType):
    image_url = String()


class AddonObject(ObjectType):
    name = String()
    description = String()
    price = Float()


class PostObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    rating = Float()
    booking_count = Int()
    company_id = Int()
    user_profile_id = Int()
    prices = List(lambda: PriceObject)
    images = List(lambda: ImageObject)
    addons = List(lambda: AddonObject)

    @staticmethod
    def resolve_prices(root, info):
        return root.prices

    @staticmethod
    def resolve_images(root, info):
        return root.images

    @staticmethod
    def resolve_addons(root, info):
        return root.addons
