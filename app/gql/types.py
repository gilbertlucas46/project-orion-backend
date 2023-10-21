from graphene import ObjectType, String, Int, List, Field

class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject) # "lambda" defer undefined class names
    
    @staticmethod
    def resolve_jobs(root, info):
        return root.jobs
    
class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda:EmployerObject) # a job is associated with a single employer
    # The next() function is used to retrieve the next item from
    # the iterable created by the generator expression. In this case, it will
    # return the first employer that matches the condition.
    @staticmethod
    def resolve_employer(root, info):
        return root.employer