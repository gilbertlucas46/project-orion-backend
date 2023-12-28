# app/gql/post/mutations.py
from graphene import Mutation, String, Int, Field, Float, List, InputObjectType
from app.db.models import User, Post, Price, Image, Addon
from app.gql.types import PostObject, AddonObject, PriceObject, ImageObject
from app.db.database import Session
from app.utils.utils import authd_user_same_as
from app.gql.enums import ServiceTypeEnum, ServiceTypeGQLEnum


class AddPost(Mutation):
    class Arguments:
        user_id = Int(required=True)
        serviceType = ServiceTypeGQLEnum(
            default_value=ServiceTypeEnum.CAR_WASH)
        description = String()
        rating = Float()
        booking_count = Int()
        prices = List(PriceObject)
        images = List(ImageObject)
        addons = List(AddonObject)

    post = Field(lambda: PostObject)

    @authd_user_same_as
    def mutate(root, info, user_id, serviceType, description, rating, booking_count, prices, images, addons):
        post = Post(
            user_id=user_id,
            serviceType=serviceType,
            description=description,
            rating=rating,
            booking_count=booking_count
        )

        for price in prices:
            post.prices.append(
                Price(vehicleType=price.vehicleType, price=price.price)
            )

        for image in images:
            post.images.append(Image(imageUrl=image.imageUrl))

        for addon in addons:
            post.addons.append(
                Addon(name=addon.name, description=addon.description, price=addon.price))

        session = Session()
        session.add(post)
        session.commit()
        session.refresh(post)
        return AddPost(post=post)

# Assuming you have input types for Price and Addon
