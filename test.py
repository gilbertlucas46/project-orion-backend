from graphene import Schema, ObjectType, String , Int, Field, List, Mutation

class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()

class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()
        
    user = Field(UserType)
    
    @staticmethod
    def mutate(root, info, user_id, name=None, age=None):
        user = None
        for u in Query.users:
            if u['id'] == user_id:
                user = u
                break

        if not user:
            return None
        
        if name is not None:
            user["name"] = name
            
        if age is not None:
            user["age"] = age
        
        return UpdateUser(user=user)
    
class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        
    user = Field(UserType)
    
    @staticmethod
    def mutate(root, info, user_id):
        user = None
        for idx, u in Query.users:
            if u['id'] == user_id:
                user = u
                del Query.users[idx]
                break #break because our assumption is theres only one of this id
        # check  if use with id exist
        if not user:
            return None
        
        return DeleteUser(user=user)

class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()
        
    user = Field(UserType)
    
    @staticmethod
    def mutate(self,info, name, age):
        user = { "id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)

class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())
    
    users = [
        {"id": 1, "name": "Gilbert", "age": 32},
        {"id": 2, "name": "Mia", "age": 34}
    ]
    
    @staticmethod
    def resolve_user(root, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None
    
    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        return [user for user in Query.users if user['age'] >= min_age]

class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

# OOP aside:
# - instance methods(self)
# - class methofs(cls)
# - staticmethod

schema = Schema(query=Query, mutation=Mutation)

gql_2 = '''
{
    user(userId: 2) {
        id
        name
        age
    }
}
# '''
# gql = '''
# {
#     usersByMinAge(minAge: 34) {
#         id
#         name
#         age
#     }
# }
# '''

gql = '''
mutation {
    createUser(name: "ungas", age: 100) {
        user {
            id
            name
            age
        }
    }
}
'''

gql_update = '''
mutation {
    updateUser(name: "ungas", age: 111, userId: 2) {
        user {
            id
            name
            age
        }
    }
}
'''

gql_delete = '''
mutation {
    deleteUser(userId: 2) {
        user {
            id
            name
            age
        }
    }
}
'''

if __name__ == "__main__":
    result = schema.execute(gql)
    print(result)
    result = schema.execute(gql_2)
    print(result)
    result = schema.execute(gql_update)
    print(result)
    result = schema.execute(gql_delete)
    print(result)