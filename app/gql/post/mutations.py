# app/gql/post/mutations.py
from graphene import Mutation, String, Int, Field, Float, List, InputObjectType
from graphql import GraphQLError
from app.db.models import Image, Post, Price, User
from app.gql.types import ImageObject, PostObject, PostPriceObject, PriceObject
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
        session = Session()

        # Check if the associated post exists
        existing_post = session.query(Post).filter_by(id=post_id).first()

        if not existing_post:
            raise GraphQLError(f"Post with ID {post_id} does not exist.")

        # Add this job to the session
        price = Price(vehicleType=vehicleType, price=price, post_id=post_id)
        session.add(price)
        session.commit()

        # Refresh the job instance with the current state in the db
        session.refresh(price)
        return AddPostPrice(price=price)


class AddPostImage(Mutation):
    class Arguments:
        imageUrl = String()
        post_id = Int(required=True)

    image = Field(lambda: ImageObject)

    @staticmethod
    def mutate(root, info, imageUrl, post_id):
        session = Session()

        # Check if the associated post exists
        existing_post = session.query(Post).filter_by(id=post_id).first()

        if not existing_post:
            raise GraphQLError(f"Post with ID {post_id} does not exist.")

        # Add this image to the session and associate it with the post
        image = Image(imageUrl=imageUrl, post=existing_post)
        session.add(image)
        session.commit()

        # Refresh the image instance with the current state in the db
        session.refresh(image)
        return AddPostImage(image=image)
