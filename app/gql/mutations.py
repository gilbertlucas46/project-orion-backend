from graphene import ObjectType
from app.gql.job.mutations import AddJob, UpdateJob, DeleteJob
from app.gql.employer.mutations import AddEmployer, UpdateEmployer
class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
