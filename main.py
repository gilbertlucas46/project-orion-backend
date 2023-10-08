from graphene import Schema, ObjectType, String , Int, Field, List, Mutation
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler

class Query(ObjectType):
    hello = String(name=String(default_value="graphql"))
    
    @staticmethod
    def resolve_hello(root, info, name):
        return f"hello {name}" 
    
schema = Schema(query=Query)

app = FastAPI()

# mount on graphql API
app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))
# at this point we are exposing our graphql API at "/graphql" endpoint of out web application