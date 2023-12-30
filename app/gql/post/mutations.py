# app/gql/post/mutations.py
from graphene import Mutation, String, Int, Field, Float, List, InputObjectType
from graphql import GraphQLError
from app.db.models import Post, Price, User
from app.gql.types import PostObject, PostPriceObject, PriceObject
from app.db.database import Session
from app.utils.utils import authd_user_same_as
from app.gql.enums import ServiceTypeEnum, ServiceTypeGQLEnum, VehicleTypeEnum, VehicleTypeGQLEnum
import graphql


class AddPost(Mutation):
    class Arguments:
        user_id = Int(required=True)
        serviceType = ServiceTypeGQLEnum(
            default_value=ServiceTypeEnum.CAR_WASH)
        description = String()
        rating = Float()
        booking_count = Int()

    post = Field(lambda: PostObject)

    @authd_user_same_as
    def mutate(root, info, user_id, serviceType, description, rating, booking_count):
        post = Post(
            user_id=user_id,
            serviceType=serviceType,
            description=description,
            rating=rating,
            booking_count=booking_count
        )

        session = Session()
        session.add(post)
        session.commit()
        session.refresh(post)
        return AddPost(post=post)


class AddPostPrice(Mutation):
    class Arguments:
        vehicleType = VehicleTypeGQLEnum(required=True)
        price = Int(required=True)
        post_id = Int(required=True)

    price = Field(lambda: PriceObject)

    @staticmethod
    def mutate(root, info, vehicleType, price, post_id):
        # add this job to the session
        price = Price(vehicleType=vehicleType, price=price, post_id=post_id)
        session = Session()

        session.add(price)
        session.commit()
        # we're refreshing the job instance with the current state that it has in the db
        session.refresh(price)
        return AddPostPrice(price=price)


class ApplyPriceToPost(Mutation):
    class Arguments:
        post_id = Int(required=True)
        user_id = Int(required=True)

    # It returns a job application field
    post_price = Field(lambda: PostPriceObject)

    @authd_user_same_as
    def mutate(root, info, user_id, post_id):
        session = Session()

        # check first if the price already exist
        existing_price = session.query(Price).filter(
            Price.user_id == user_id,
            Price.post_id == post_id,
        ).first()

        if existing_price:
            raise GraphQLError("This user has already applied to this job")

        # Price -> database model, create new instance
        post_price = Price(post_id=post_id)
        session.add(post_price)
        session.commit()
        # Refresh it in order to get the ID that Porsgres assigned
        session.refresh(post_price)

        return ApplyPriceToPost(post_price=post_price)
