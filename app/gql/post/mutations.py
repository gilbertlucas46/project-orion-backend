from graphene import Mutation, String, Int, Field, Boolean, Float
from app.gql.types import PostObject
from app.db.database import Session
from app.db.models import Post
from app.utils.utils import admin_user


class AddPost(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        rating = Float(required=True)
        booking_count = Int(required=True)

    post = Field(lambda: PostObject)

    @admin_user
    def mutate(root, info, title, description, rating, booking_count):
        post = Post(title=title, description=description,
                    rating=rating, booking_count=booking_count)
        session = Session()
        session.add(post)
        session.commit()
        session.refresh(post)
        return AddPost(post=post)
