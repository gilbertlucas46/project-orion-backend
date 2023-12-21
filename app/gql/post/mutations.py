from graphene import Mutation, String, Int, Field, Boolean, Float
from app.gql.types import PostObject
from app.gql.types import UserObject
from app.db.models import User
from app.db.database import Session
from app.db.models import Post
from app.utils.utils import authd_user_same_as, authd_user_same_as_id
from app.db.data import bookings


class AddPost(Mutation):
    class Arguments:
        user_id = Int(required=True)
        title = String()
        description = String()
        rating = Float()
        booking_count = Int()

    post = Field(lambda: PostObject)

    @authd_user_same_as
    def mutate(root, info, user_id, title, description, rating, booking_count):
        post = Post(user_id=user_id, title=title, description=description,
                    rating=rating, booking_count=booking_count)  # add this job to the session
        session = Session()
        session.add(post)
        session.commit()
        # we're refreshing the job instance with the current state that it has in the db
        session.refresh(post)
        return AddPost(post=post)
