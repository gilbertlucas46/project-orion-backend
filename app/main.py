from graphene import Schema
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
from app.db.database import prepare_database, Session
from app.gql.queries import Query
from app.db.models import Employer, Job
from app.gql.mutations import Mutation
 
schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()

#Fast api provides some special decorators to let us hook into the
#varios application events, and one such event is startup, which is triggered
#when the application, well literally starts up.

@app.on_event("startup")
def startup_event():
    prepare_database()
    
@app.get("/employers")
def get_employers():
    with Session() as session:
        return session.query(Employer).all()
    
@app.get("/jobs")
def get_employers():
    with Session() as session:
        return session.query(Job).all()

# mount on graphql API
app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))
# at this point we are exposing our graphql API at "/graphql" endpoint of out web application