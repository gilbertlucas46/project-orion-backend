from graphene import Schema
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp, make_playground_handler
from app.db.database import prepare_database, Session
from app.gql.queries import Query
from app.db.models import Employer, Job
from app.gql.mutations import Mutation

schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()

# FastAPI provides some special decorators to let us hook into the
# various application events, and one such event is startup, which is triggered
# when the application, well literally starts up.


@app.on_event("startup")
def startup_event():
    prepare_database()


# CORS middleware settings
origins = [
    "http://localhost",    # Adjust the allowed origins as needed
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount on GraphQL API
app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))
# at this point, we are exposing our GraphQL API at "/graphql" endpoint of our web application
