# app/gql/post/mutations.py
from graphene import Mutation, String, Int, Field, Float, List
from graphql import GraphQLError
from app.db.models import Image, Post, Price, User
from app.gql.types import ImageInputObject, ImageObject, PostObject, PriceObject
from app.db.database import Session
from app.utils.utils import authd_user_same_as
from app.gql.enums import ServiceTypeEnum, ServiceTypeGQLEnum, VehicleTypeGQLEnum
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


# app/gql/post/mutations.py
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

        # Check if there is already a price with the same vehicle type for this post
        existing_price = session.query(Price).filter(
            Price.post_id == post_id,
            Price.vehicleType == vehicleType
        ).first()

        if existing_price:
            raise GraphQLError(
                f"A price with vehicle type {vehicleType} already exists for this post.")

        # Add this price to the session
        price = Price(vehicleType=vehicleType, price=price, post_id=post_id)
        session.add(price)
        session.commit()

        # Refresh the price instance with the current state in the db
        session.refresh(price)
        return AddPostPrice(price=price)


class AddPostImage(Mutation):
    class Arguments:
        post_id = Int(required=True)
        images = List(ImageInputObject, required=True)

    images = List(lambda: ImageObject)

    @staticmethod
    def mutate(root, info, post_id, images):
        session = Session()

        # Check if the associated post exists
        existing_post = session.query(Post).filter_by(id=post_id).first()

        if not existing_post:
            raise GraphQLError(f"Post with ID {post_id} does not exist.")

        # Add multiple images to the session and associate them with the post
        image_objects = [
            Image(imageUrl=image["imageUrl"], post=existing_post) for image in images
        ]

        session.add_all(image_objects)
        session.commit()

        # Refresh each image instance with the current state in the db
        for image_object in image_objects:
            session.refresh(image_object)

        return AddPostImage(images=image_objects)
