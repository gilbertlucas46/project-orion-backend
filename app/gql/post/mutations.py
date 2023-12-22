# app/gql/post/mutations.py
from graphene import Mutation, String, Int, Field, Float, List, InputObjectType
from app.db.models import User, Post, Price, Image, Addon
from app.gql.types import PostObject, AddonObject, PriceObject, ImageObject
from app.db.database import Session
from app.utils.utils import authd_user_same_as


class AddPost(Mutation):
    class Arguments:
        user_id = Int(required=True)
        title = String()
        description = String()
        rating = Float()
        booking_count = Int()
        prices = List(PriceObject)  # Assuming you have an input type for Price
        images = List(ImageObject)
        addons = List(AddonObject)  # Assuming you have an input type for Addon

    post = Field(lambda: PostObject)

    @authd_user_same_as
    def mutate(root, info, user_id, title, description, rating, booking_count, prices, images, addons):
        post = Post(
            user_id=user_id,
            title=title,
            description=description,
            rating=rating,
            booking_count=booking_count
        )

        for price in prices:
            post.prices.append(
                Price(vehicle_type=price.vehicle_type, price=price.price))

        for image in images:
            post.images.append(Image(image_url=image.image_url))

        for addon in addons:
            post.addons.append(
                Addon(name=addon.name, description=addon.description, price=addon.price))

        session = Session()
        session.add(post)
        session.commit()
        session.refresh(post)
        return AddPost(post=post)

# Assuming you have input types for Price and Addon
