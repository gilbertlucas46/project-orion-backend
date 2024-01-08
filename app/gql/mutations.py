from graphene import ObjectType
from app.gql.job.mutations import AddJob, UpdateJob, DeleteJob
from app.gql.post.mutations import AddPost, AddPostAddon, AddPostImage, AddPostPrice
from app.gql.employer.mutations import AddEmployer, UpdateEmployer, DeleteEmployer
from app.gql.user.mutations import LoginUser, AddUser, ApplyToJob, UpdateUser


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    login_user = LoginUser.Field()
    add_user = AddUser.Field()
    apply_to_jobs = ApplyToJob.Field()
    add_post = AddPost.Field()
    add_post_price = AddPostPrice.Field()
    update_user = UpdateUser.Field()
    add_post_image = AddPostImage.Field()
    add_post_addon = AddPostAddon.Field()
